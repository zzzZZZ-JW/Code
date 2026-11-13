"""按原实验报告模板填写；保留原模板，另存完成版。

使用 Codex 文档运行时的 Python 执行。输入为 run_experiment.py 的真实结果
及浏览器截图；本脚本不会自行运行实验或伪造运行截图。
"""

from copy import deepcopy
import hashlib
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


CODE = Path(__file__).resolve().parent
MATERIALS = Path.home() / "Library/CloudStorage/OneDrive-个人/资料/人工智能专业导论"
SOURCE = MATERIALS / "实验四/2506456052-张佳伟-实验四.docx"
OUTPUT = SOURCE.with_name("2506456052-张佳伟-实验四-完成版.docx")
RESULTS = MATERIALS / "实验四/运行结果"
EXPECTED_SHA = "2f3b359df56ec7ad5f94810bbe611608d47aece31dac93a5b9cc94b55ba25fef"


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA
    results = json.loads((RESULTS / "results.json").read_text())
    assert results["test_exit_code"] == 0
    assert [c["result"]["cost"] for c in results["cases"]] == [7, 7, 7, 9, 9]
    for name in ["baseline-screenshot.png", "comparison-screenshot.png", "search_process.png"]:
        assert (RESULTS / name).is_file(), name
    d = Document(SOURCE)
    original = list(d.paragraphs)
    original_sections = [deepcopy(s._sectPr) for s in d.sections]
    original_metadata = deepcopy(d.tables[0]._tbl)

    # 仅纠正实验名称；其他元数据按用户已经填写的模板保留。
    name_nodes = d.tables[1].cell(0, 1)._tc.xpath('.//w:t')
    name_nodes[0].text = "实验四 搜索算法实现"
    for node in name_nodes[1:]:
        node.text = ""
    assert "实验四 搜索算法实现" in d.tables[1].cell(0, 1).text

    def format_paragraph(p, code=False, heading=False):
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0 if code else 2)
        pf.line_spacing = Pt(11 if code else 14)
        pf.keep_with_next = heading
        pf.keep_together = False
        pf.page_break_before = False
        pr = p._p.get_or_add_pPr()
        snap = pr.find(qn("w:snapToGrid"))
        if snap is None:
            snap = OxmlElement("w:snapToGrid")
            pr.append(snap)
        snap.set(qn("w:val"), "false")
        spacing = pr.find(qn("w:spacing"))
        if spacing is not None:
            for attr in ["beforeLines", "afterLines", "beforeAutospacing", "afterAutospacing"]:
                spacing.attrib.pop(qn("w:" + attr), None)
        for run in p.runs:
            run.font.name = "Courier New" if code else "Times New Roman"
            run.font.size = Pt(9 if code else 10.5)
            run.font.color.rgb = RGBColor(0, 0, 0)
            run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "宋体")
            if heading:
                run.bold = True

    original[11].text = (
        "h(n)：从当前节点到目标节点的估计代价。边权非负、h(目标)=0 时，"
        "可采纳性要求 h(n) 不超过真实最短剩余代价；图搜索若发现更小 g(n)，应允许重开节点。"
        "若关闭后不再重开，则还需启发函数满足一致性 h(u)≤w(u,v)+h(v)。")
    original[13].text = "关闭列表：记录已展开节点；发现通往该节点的更低代价时，将其重新加入开放列表。"
    for i, p in enumerate(original):
        if i >= 4:
            format_paragraph(p, heading=i in [4, 8, 21, 24])
    for i in [22, 23]:
        original[i]._p.getparent().remove(original[i]._p)
    anchor = original[24]

    def add(text="", heading=False, code=False):
        p = anchor.insert_paragraph_before(text, style="Normal")
        format_paragraph(p, code, heading)
        p.paragraph_format.left_indent = Pt(0)
        p.paragraph_format.right_indent = Pt(0)
        p.paragraph_format.first_line_indent = Pt(0)
        return p

    def code(text):
        for line in text.strip("\n").splitlines():
            if line.strip():
                p = add(line, code=True)
                if line.rstrip().endswith(("(", ":")) or line.startswith("POSITIONS ="):
                    p.paragraph_format.keep_with_next = True

    def picture(filename, caption):
        p = add()
        p.alignment = 1
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.keep_with_next = True
        shape = p.add_run().add_picture(str(RESULTS / filename), width=Cm(15.4))
        shape._inline.docPr.set("descr", caption)
        caption_p = add(caption)
        caption_p.alignment = 1
        for r in caption_p.runs:
            r.font.size = Pt(9)

    core_source = (CODE / "astar_search.py").read_text()
    add("1  实验环境与图结构", heading=True)
    add("本次使用 macOS arm64、Python 3.13.9、NetworkX 3.5 和 Matplotlib 3.10.6。"
        "图使用讲义给出的五个节点及六条无向边，起点为 A，终点为 E。代码存放于 "
        "Introduction to AI/lab4；执行 python run_experiment.py 生成运行日志、图像和五组对照结果。")
    code(core_source[core_source.index("GRAPH ="):core_source.index("@dataclass")].strip())
    add("原曼哈顿启发值为 A=6、B=5、C=5、D=2、E=0。坐标用于绘图，边权表示实际代价，"
        "两者并非同一尺度，因此后续还要检查启发函数是否高估。")

    add("2  A* 搜索核心实现", heading=True)
    add("使用 heapq 维护开放列表，按 f=g+h 选取节点，同 f 时按节点名称排序。g 保存当前最小已知代价，"
        "parent 保存前驱，SearchResult 保存路径、代价及搜索记录。以下为实际程序的搜索循环，省略输入校验和绘图用的步骤快照。")
    search_loop = core_source[core_source.index("    open_heap ="):core_source.index("        # 用有效堆条目")]
    code("def a_star_search(graph, start, goal, heuristic):\n" + search_loop
         + "        if current == goal:\n            return result\n    return result")
    add("起点以 h(A)=6 入堆，修正讲义首步 f(A)=0 与定义不一致的问题。堆条目保留入堆时的 g，"
        "弹出时跳过旧条目；发现更小 g 时重开关闭节点，避免不一致启发函数下过早锁定路径。"
        "程序返回真实 search_steps，过程图直接读取该记录。")

    add("3  运行结果与搜索过程", heading=True)
    add("图1为结果页面的实际浏览器截图。搜索依次选取 A、B、C、D、E，最终路径为 "
        "A→B→C→D→E，总代价 1+2+1+3=7。选取数为5，包含目标 E；真正展开邻居的次数为4。"
        "截图中的 OPEN 和 CLOSED 均为当前步骤处理后的状态。")
    picture("baseline-screenshot.png", "图1  实际搜索日志 图结构与返回路径")
    add("可视化使用 NetworkX 绘制节点和带权边，再将最终路径着色；过程图选取真实记录中的第1、3、4步。核心调用如下：")
    code('''network = networkx_graph(graph)
nx.draw_networkx_edges(network, POSITIONS, ax=ax)
nx.draw_networkx_nodes(network, POSITIONS, ax=ax, node_color=colors)
nx.draw_networkx_labels(network, POSITIONS, ax=ax)
nx.draw_networkx_edge_labels(network, POSITIONS, ax=ax,
    edge_labels=nx.get_edge_attributes(network, "weight"))
path_edges = list(zip(result.path, result.path[1:]))
nx.draw_networkx_edges(network, POSITIONS, ax=ax,
    edgelist=path_edges, edge_color="red", width=3)''')
    picture("search_process.png", "图2  实际搜索过程 红色为当前节点 黄色为开放节点 灰色为关闭节点")
    add("A 展开后 B、C 进入 OPEN；B 将 C 的 g 从4降至3，同时发现代价6到达 D 的路线；"
        "C 再将 D 的 g 降至4，D 随后将 E 的 g 更新为7。父节点最终连成 A—B—C—D—E。")

    add("4  思考题 修改启发函数与图结构", heading=True)
    add("保持起终点和同分排序规则不变，分别使用原曼哈顿、零启发、1/3曼哈顿和2倍曼哈顿；"
        "另将无向边 C—D 的两个方向权重均由1改为8。每组均重新搜索，并用 NetworkX 的 Dijkstra 最短代价核对。")
    picture("comparison-screenshot.png", "图3  五组实际对照结果及测试通过记录")
    add("（1）原图从 A、B、C、D、E 到终点的真实最短代价分别为7、6、4、3、0。原启发函数 "
        "h(C)=5>4，不满足可采纳性；C→D 还有 5>1+2，不满足一致性。原例仍得到代价7，"
        "但不能据此推断这种距离定义总能保证最优。")
    add("（2）零启发令 f=g，相当于 Dijkstra。将曼哈顿距离乘以1/3后，每条边均满足 "
        "d₁(u,v)/3≤w(u,v)，由三角不等式可知启发函数一致，因而可采纳。"
        "本图中这两组与原启发均选取5个节点，没有观察到搜索量减少。")
    add("（3）2倍曼哈顿产生 h={A:12,B:10,C:10,D:4,E:0}。展开 B 后，D 的 f=6+4=10 "
        "小于 C 的 f=3+10=13；随后 E 的 f=9，先于 C 被选取。算法返回 A→B→D→E，代价9，"
        "虽然少展开1个节点，却失去最优性。")
    add("（4）将 C—D 权重改为8后，原路径代价升为14，而 A→B→D→E 的代价仍为9，"
        "因此最优路径改变。这组的真实剩余代价为9、8、10、3、0，原曼哈顿在新图上也满足一致性；"
        "返回代价9是正确结果，与前一组因高估导致的次优结果不同。")
    add("此外，8项测试覆盖讲义示例、起终点相同、目标不可达、节点重开、过期堆条目、"
        "高估反例、修改边权和拒绝负权。可采纳但不一致的测试中，重开节点后获得代价5，"
        "避免将原先代价6的路线作为最终结果。")

    anchor = original[25]
    add("本次完成了图构建、A* 搜索、路径回溯和真实过程可视化。实现中重点处理了首节点 f 值、"
        "过期堆条目和关闭节点重开三个问题，使输出与评估函数定义一致，节点统计也不会被旧条目重复计入。")
    add("对照实验表明，启发函数必须结合实际边权检查，绘图距离不能直接视为可靠的剩余代价。"
        "高估可能减少搜索量，也可能让算法更早返回次优路径；本例中改用可采纳启发函数并未减少节点数，"
        "因此不能仅凭一张小图判断效率优势。后续比较更大图时，还应统一节点统计口径并考虑图结构、启发质量和运行时间。")
    original[25]._p.getparent().remove(original[25]._p)
    if not original[26].text and not original[26]._p.xpath('.//w:sectPr'):
        original[26]._p.getparent().remove(original[26]._p)

    settings = d.settings.element
    update = settings.find(qn("w:updateFields"))
    if update is None:
        update = OxmlElement("w:updateFields")
        settings.append(update)
    update.set(qn("w:val"), "true")
    canonical = lambda element: etree.tostring(element, method="c14n", exclusive=True)
    assert [canonical(s._sectPr) for s in d.sections] == [canonical(s) for s in original_sections]
    assert canonical(d.tables[0]._tbl) == canonical(original_metadata)
    memory = BytesIO()
    d.save(memory)
    editable = {"word/document.xml", "word/_rels/document.xml.rels",
                "[Content_Types].xml", "word/settings.xml"}
    with ZipFile(SOURCE) as source, ZipFile(memory) as edited, ZipFile(OUTPUT, "w", ZIP_DEFLATED) as out:
        for name in source.namelist():
            out.writestr(name, edited.read(name) if name in editable else source.read(name))
        for name in edited.namelist():
            if name not in source.namelist():
                assert name.startswith("word/media/")
                out.writestr(name, edited.read(name))
    with ZipFile(SOURCE) as source, ZipFile(OUTPUT) as final:
        for name in source.namelist():
            if name not in editable:
                assert source.read(name) == final.read(name), name
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA
    print(OUTPUT)
    print("PASS: original metadata, sections and preserve-only package parts unchanged")


if __name__ == "__main__":
    main()
