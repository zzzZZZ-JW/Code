import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import type { JointKey } from "./types";

interface RobotSceneProps {
  joints: Record<JointKey, number>;
  selectedJoint: JointKey;
}

const JOINT_ORDER: JointKey[] = [
  "shoulder_pan.pos",
  "shoulder_lift.pos",
  "elbow_flex.pos",
  "wrist_flex.pos",
  "wrist_roll.pos",
  "gripper.pos"
];

type LinkName = "base" | "shoulder" | "upperArm" | "lowerArm" | "wrist" | "gripper" | "jaw";
type ChildLinkName = Exclude<LinkName, "base">;

interface JointSpec {
  key: JointKey;
  parent: LinkName;
  child: ChildLinkName;
  valueToDegrees: (value: number) => number;
}

interface JointGuide {
  group: THREE.Group;
  normal: THREE.Group;
  active: THREE.Group;
}

interface RobotRig {
  links: Record<LinkName, THREE.Object3D>;
  restMatrices: Record<LinkName, THREE.Matrix4>;
  relativeMatrices: Record<ChildLinkName, THREE.Matrix4>;
  jointGuides: Record<JointKey, JointGuide>;
}

const MODEL_URL = "/models/so101_new_calib.glb";

const LINK_NAMES: LinkName[] = ["base", "shoulder", "upperArm", "lowerArm", "wrist", "gripper", "jaw"];

const LINK_OBJECT_NAMES: Record<LinkName, string> = {
  base: "base",
  shoulder: "shoulder",
  upperArm: "upper_arm",
  lowerArm: "lower_arm",
  wrist: "wrist",
  gripper: "gripper",
  jaw: "moving_jaw_so101_v1"
};

const JOINT_SPECS: JointSpec[] = [
  { key: "shoulder_pan.pos", parent: "base", child: "shoulder", valueToDegrees: degreesValue },
  { key: "shoulder_lift.pos", parent: "shoulder", child: "upperArm", valueToDegrees: degreesValue },
  { key: "elbow_flex.pos", parent: "upperArm", child: "lowerArm", valueToDegrees: degreesValue },
  { key: "wrist_flex.pos", parent: "lowerArm", child: "wrist", valueToDegrees: degreesValue },
  { key: "wrist_roll.pos", parent: "wrist", child: "gripper", valueToDegrees: degreesValue },
  { key: "gripper.pos", parent: "gripper", child: "jaw", valueToDegrees: gripperValueToDegrees }
];

// The source USD declares each revolute joint on Z; the GLB conversion maps that local axis to Y.
const USD_Z_AXIS_IN_GLB_LINK_SPACE = new THREE.Vector3(0, 1, 0);

export default function RobotScene({ joints, selectedJoint }: RobotSceneProps) {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const sceneRef = useRef<{
    renderer: THREE.WebGLRenderer;
    camera: THREE.PerspectiveCamera;
    scene: THREE.Scene;
    controls: OrbitControls;
    robotRig: RobotRig | null;
    animationId: number;
  } | null>(null);

  useEffect(() => {
    if (!hostRef.current) return;

    const host = hostRef.current;
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f1413);

    const camera = new THREE.PerspectiveCamera(42, 1, 0.08, 100);
    camera.position.set(2.4, 1.7, 3.0);
    camera.lookAt(0, 0.95, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    host.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.target.set(0, 0.95, 0);
    controls.minDistance = 1.25;
    controls.maxDistance = 5.8;
    controls.maxPolarAngle = Math.PI * 0.88;

    scene.add(new THREE.HemisphereLight(0xe6eee9, 0x202726, 2.15));

    const keyLight = new THREE.DirectionalLight(0xffedbf, 3.3);
    keyLight.position.set(4.5, 6, 3.2);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    scene.add(keyLight);

    const fill = new THREE.PointLight(0x59d7b5, 18, 8);
    fill.position.set(-2.2, 1.6, 2.4);
    scene.add(fill);

    const rim = new THREE.DirectionalLight(0x83bfff, 1.25);
    rim.position.set(-3.5, 3.2, -3.2);
    scene.add(rim);

    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(2.4, 96),
      new THREE.MeshStandardMaterial({ color: 0x1a211f, metalness: 0.08, roughness: 0.82 })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    const grid = new THREE.GridHelper(4.8, 24, 0x4d5f58, 0x27342f);
    grid.position.y = 0.006;
    scene.add(grid);

    const loader = new GLTFLoader();
    loader.load(
      MODEL_URL,
      (gltf) => {
        const model = gltf.scene;
        prepareModel(model);
        scaleModelForStage(model);
        scene.add(model);

        const rig = buildRobotRig(model);
        if (!rig) return;

        const current = sceneRef.current;
        if (current) {
          current.robotRig = rig;
          applyRobotPose(rig, joints);
          updateJointGuideSelection(rig, selectedJoint);
        }
      },
      undefined,
      (error) => {
        console.error("Failed to load SO101 preview model", error);
      }
    );

    const resize = () => {
      const width = Math.max(host.clientWidth, 320);
      const height = Math.max(host.clientHeight, 320);
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    };
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(host);
    resize();

    const render = () => {
      controls.update();
      renderer.render(scene, camera);
      const current = sceneRef.current;
      if (current) current.animationId = requestAnimationFrame(render);
    };

    sceneRef.current = {
      renderer,
      camera,
      scene,
      controls,
      robotRig: null,
      animationId: requestAnimationFrame(render)
    };

    return () => {
      const current = sceneRef.current;
      if (current) cancelAnimationFrame(current.animationId);
      resizeObserver.disconnect();
      controls.dispose();
      renderer.dispose();
      host.removeChild(renderer.domElement);
      scene.traverse(disposeObject);
      sceneRef.current = null;
    };
  }, []);

  useEffect(() => {
    const refs = sceneRef.current;
    if (!refs?.robotRig) return;
    applyRobotPose(refs.robotRig, joints);
  }, [joints]);

  useEffect(() => {
    const refs = sceneRef.current;
    if (!refs?.robotRig) return;
    updateJointGuideSelection(refs.robotRig, selectedJoint);
  }, [selectedJoint]);

  return <div ref={hostRef} className="robot-scene" aria-label="SO-ARM101 三维模型" />;
}

function prepareModel(model: THREE.Object3D) {
  model.traverse((obj) => {
    if (isHiddenUsdNode(obj)) {
      obj.visible = false;
    }

    if (obj instanceof THREE.Mesh) {
      obj.castShadow = true;
      obj.receiveShadow = true;
      obj.material = normalizeMaterial(obj.material);
    }
  });
}

function normalizeMaterial(material: THREE.Material | THREE.Material[]) {
  if (Array.isArray(material)) return material.map(normalizeSingleMaterial);
  return normalizeSingleMaterial(material);
}

function normalizeSingleMaterial(material: THREE.Material) {
  if (material instanceof THREE.MeshStandardMaterial) {
    const next = material.clone();
    next.metalness = Math.min(next.metalness, 0.18);
    next.roughness = Math.max(next.roughness, 0.56);
    next.transparent = false;
    next.opacity = 1;
    return next;
  }

  return new THREE.MeshStandardMaterial({ color: 0xe7d36c, metalness: 0.08, roughness: 0.62 });
}

function scaleModelForStage(model: THREE.Object3D) {
  const box = visibleBox(model);
  const size = box.getSize(new THREE.Vector3());
  const maxSize = Math.max(size.x, size.y, size.z) || 1;
  model.scale.setScalar(2.35 / maxSize);
  anchorModelToFloor(model);
}

function anchorModelToFloor(model: THREE.Object3D) {
  model.updateWorldMatrix(true, true);
  const box = visibleBox(model);
  const center = box.getCenter(new THREE.Vector3());
  model.position.x -= center.x;
  model.position.z -= center.z;
  model.position.y -= box.min.y;
  model.updateWorldMatrix(true, true);
}

function visibleBox(model: THREE.Object3D) {
  const box = new THREE.Box3();
  model.updateWorldMatrix(true, true);
  model.traverse((obj) => {
    if (!(obj instanceof THREE.Mesh) || !obj.visible) return;
    obj.updateWorldMatrix(true, false);
    const geometry = obj.geometry;
    if (!geometry.boundingBox) geometry.computeBoundingBox();
    const geometryBox = geometry.boundingBox?.clone();
    if (geometryBox) box.union(geometryBox.applyMatrix4(obj.matrixWorld));
  });
  return box.isEmpty() ? new THREE.Box3().setFromObject(model) : box;
}

function buildRobotRig(model: THREE.Object3D): RobotRig | null {
  const links = Object.fromEntries(
    LINK_NAMES.map((name) => [name, model.getObjectByName(LINK_OBJECT_NAMES[name])])
  ) as Partial<Record<LinkName, THREE.Object3D>>;

  if (LINK_NAMES.some((name) => !links[name])) return null;

  const typedLinks = links as Record<LinkName, THREE.Object3D>;
  const commonParent = typedLinks.base.parent;
  if (!commonParent || LINK_NAMES.some((name) => typedLinks[name].parent !== commonParent)) return null;

  for (const linkObject of Object.values(typedLinks)) {
    linkObject.updateMatrix();
  }

  const restMatrices = Object.fromEntries(
    LINK_NAMES.map((name) => [name, typedLinks[name].matrix.clone()])
  ) as Record<LinkName, THREE.Matrix4>;

  const relativeMatrices = Object.fromEntries(
    JOINT_SPECS.map((joint) => [joint.child, relativeMatrix(restMatrices[joint.parent], restMatrices[joint.child])])
  ) as Record<ChildLinkName, THREE.Matrix4>;

  const jointGuides = createJointGuides(commonParent);

  return {
    links: typedLinks,
    restMatrices,
    relativeMatrices,
    jointGuides
  };
}

function createJointGuides(parent: THREE.Object3D) {
  const guides = {} as Record<JointKey, JointGuide>;

  for (const joint of JOINT_SPECS) {
    const group = new THREE.Group();
    group.name = `${joint.key}-rotation-guide`;

    const normal = rotationGuideVisual(0.032, 0x5bd6c0, 0.44);
    const active = rotationGuideVisual(0.042, 0xf2c95f, 0.98);
    active.visible = false;

    group.add(normal, active);
    parent.add(group);
    guides[joint.key] = { group, normal, active };
  }

  return guides;
}

function rotationGuideVisual(radius: number, color: number, opacity: number) {
  const group = new THREE.Group();
  const material = new THREE.LineBasicMaterial({
    color,
    transparent: true,
    opacity,
    depthTest: false
  });

  const points: THREE.Vector3[] = [];
  const start = -Math.PI * 0.7;
  const end = Math.PI * 0.92;
  const steps = 34;
  for (let i = 0; i <= steps; i += 1) {
    const theta = THREE.MathUtils.lerp(start, end, i / steps);
    points.push(new THREE.Vector3(Math.cos(theta) * radius, 0, Math.sin(theta) * radius));
  }

  const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), material);
  line.renderOrder = 10;
  group.add(line);

  const endPoint = points[points.length - 1];
  const tangent = new THREE.Vector3(-Math.sin(end), 0, Math.cos(end)).normalize();
  const arrow = new THREE.ArrowHelper(tangent, endPoint, radius * 0.58, color, radius * 0.28, radius * 0.24);
  setGuideOpacity(arrow, opacity);
  arrow.renderOrder = 10;
  group.add(arrow);

  const pivot = new THREE.Mesh(
    new THREE.SphereGeometry(radius * 0.16, 14, 10),
    new THREE.MeshBasicMaterial({ color, transparent: true, opacity, depthTest: false })
  );
  pivot.renderOrder = 10;
  group.add(pivot);

  return group;
}

function setGuideOpacity(object: THREE.Object3D, opacity: number) {
  object.traverse((child) => {
    const material = materialOf(child);
    if (!material) return;
    for (const item of Array.isArray(material) ? material : [material]) {
      item.transparent = true;
      item.opacity = opacity;
      item.depthTest = false;
    }
  });
}

function applyRobotPose(rig: RobotRig, joints: Record<JointKey, number>) {
  const poseMatrices = {
    base: rig.restMatrices.base.clone(),
    shoulder: new THREE.Matrix4(),
    upperArm: new THREE.Matrix4(),
    lowerArm: new THREE.Matrix4(),
    wrist: new THREE.Matrix4(),
    gripper: new THREE.Matrix4(),
    jaw: new THREE.Matrix4()
  } satisfies Record<LinkName, THREE.Matrix4>;

  for (const joint of JOINT_SPECS) {
    const value = joints[joint.key] ?? 0;
    poseMatrices[joint.child] = placeLink(
      poseMatrices[joint.parent],
      rig.relativeMatrices[joint.child],
      joint.valueToDegrees(value)
    );
  }

  for (const name of LINK_NAMES) {
    applyLocalMatrix(rig.links[name], poseMatrices[name]);
  }

  for (const joint of JOINT_SPECS) {
    applyLocalMatrix(rig.jointGuides[joint.key].group, poseMatrices[joint.child]);
  }
}

function updateJointGuideSelection(rig: RobotRig, selectedJoint: JointKey) {
  for (const joint of JOINT_SPECS) {
    const guide = rig.jointGuides[joint.key];
    guide.normal.visible = joint.key !== selectedJoint;
    guide.active.visible = joint.key === selectedJoint;
  }
}

function relativeMatrix(parentMatrix: THREE.Matrix4, childMatrix: THREE.Matrix4) {
  return parentMatrix.clone().invert().multiply(childMatrix);
}

function placeLink(parentMatrix: THREE.Matrix4, relativeToParent: THREE.Matrix4, degrees: number) {
  return parentMatrix
    .clone()
    .multiply(relativeToParent)
    .multiply(new THREE.Matrix4().makeRotationAxis(USD_Z_AXIS_IN_GLB_LINK_SPACE, THREE.MathUtils.degToRad(degrees)));
}

function applyLocalMatrix(linkObject: THREE.Object3D, matrix: THREE.Matrix4) {
  matrix.decompose(linkObject.position, linkObject.quaternion, linkObject.scale);
  linkObject.updateMatrix();
  linkObject.updateWorldMatrix(false, true);
}

function isHiddenUsdNode(obj: THREE.Object3D) {
  let cursor: THREE.Object3D | null = obj;
  while (cursor) {
    if (cursor.name.startsWith("collisions") || cursor.name === "joints" || cursor.name === "Looks" || cursor.name === "root_joint") {
      return true;
    }
    cursor = cursor.parent;
  }
  return obj.type === "Mesh" && !obj.parent?.name.startsWith("visuals");
}

function disposeObject(obj: THREE.Object3D) {
  if (!(obj instanceof THREE.Mesh) && !(obj instanceof THREE.Line)) return;
  obj.geometry.dispose();

  const material = materialOf(obj);
  if (Array.isArray(material)) material.forEach((item) => item.dispose());
  else material?.dispose();
}

function materialOf(obj: THREE.Object3D) {
  if (!("material" in obj)) return null;
  return obj.material as THREE.Material | THREE.Material[];
}

function degreesValue(value: number) {
  return Number(value ?? 0);
}

function gripperValueToDegrees(value: number) {
  return THREE.MathUtils.clamp(Number(value ?? 0), 0, 1) * 100;
}

export { JOINT_ORDER };
