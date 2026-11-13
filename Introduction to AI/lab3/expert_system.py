from decimal import Decimal
import platform


class AcupunctureProductionSystem:
    def __init__(self):
        self.facts = {}
        self.rules = []
        self.recommendations = {}

    def add_fact(self, symptom, confidence=1.0):
        value = Decimal(str(confidence))
        if not value.is_finite() or not 0 <= value <= 1:
            raise ValueError('置信度必须在 0 到 1 之间')
        self.facts[symptom] = value

    def add_rule(self, symptoms, acupoint, confidence=1.0):
        value = Decimal(str(confidence))
        if not symptoms or not value.is_finite() or not 0 <= value <= 1:
            raise ValueError('规则条件不能为空，置信度须在 0 到 1 之间')
        self.rules.append((tuple(symptoms), acupoint, value))

    def run(self, priority=False):
        self.recommendations = {}
        rules = sorted(self.rules, key=lambda r: r[2], reverse=True) \
                if priority else self.rules
        changed = True
        while changed:
            changed = False
            for symptoms, acupoint, weight in rules:
                if not all(self.facts.get(s, 0) > Decimal('0.5')
                           for s in symptoms):
                    continue
                evidence = min(self.facts[s] for s in symptoms)
                score = weight * evidence
                old = self.recommendations.get(acupoint, Decimal('0'))
                if score > old:
                    self.recommendations[acupoint] = score
                    changed = True
                    print(f'触发：{"且".join(symptoms)} → {acupoint}')
                    print(f'  {weight} × {evidence} = {score}；更新成功')
        print('最终推荐：', ', '.join(
            f'{name}={score:.3f}'
            for name, score in self.recommendations.items()) or '无')
        return dict(self.recommendations)


def make_system(facts, rules):
    system = AcupunctureProductionSystem()
    for symptom, confidence in facts.items():
        system.add_fact(symptom, confidence)
    for symptoms, acupoint, confidence in rules:
        system.add_rule(symptoms, acupoint, confidence)
    return system


def demo(case):
    print(f'Python {platform.python_version()} | {platform.system()} {platform.machine()}')
    if case == 1:
        print('实验题 1：合取条件与最小置信度')
        print('输入：头痛=0.8，牙痛=0.6；规则置信度=0.9')
        system = make_system({'头痛': 0.8, '牙痛': 0.6},
            [(['头痛', '牙痛'], '合谷', 0.9)])
        assert system.run() == {'合谷': Decimal('0.54')}
        print('断言通过：合谷 = 0.540')
        for title, facts in [('缺少牙痛', {'头痛': 0.8}),
                             ('牙痛等于阈值', {'头痛': 0.8, '牙痛': 0.5})]:
            print(f'边界测试：{title}')
            assert make_system(facts, [(['头痛','牙痛'],'合谷',0.9)]).run() == {}
        print('3/3 项检查通过')
    elif case == 2:
        print('实验题 2：新增风池规则')
        print('输入：鼻塞=0.8，流涕=0.7；规则置信度=0.85')
        system = make_system({'鼻塞': 0.8, '流涕': 0.7},
            [(['鼻塞', '流涕'], '风池', 0.85)])
        assert system.run() == {'风池': Decimal('0.595')}
        print('断言通过：风池 = 0.595（保留两位小数为 0.60）')
        print('边界测试：缺少流涕')
        assert make_system({'鼻塞': 0.8},
            [(['鼻塞','流涕'],'风池',0.85)]).run() == {}
        print('2/2 项检查通过')
    elif case == 3:
        print('实验题 3：按规则置信度降序执行')
        facts = {'头痛': 0.8, '便秘': 0.7, '胃痛': 0.9}
        rules = [(['便秘'], '合谷', 0.8),
                 (['头痛'], '合谷', 0.9),
                 (['胃痛'], '足三里', 0.95)]
        print('添加顺序：便秘 0.8 → 头痛 0.9 → 胃痛 0.95')
        print('A 按添加顺序执行')
        a = make_system(facts, rules).run()
        print('B 按规则置信度降序执行')
        b = make_system(facts, rules).run(priority=True)
        assert a == b == {'合谷': Decimal('0.72'), '足三里': Decimal('0.855')}
        print('断言通过：两种顺序最终结果一致；B 优先触发足三里')
        print('结果：合谷=0.720，足三里=0.855（两位小数 0.86）')
        print('1/1 项检查通过')


if __name__ == '__main__':
    import sys
    demo(int(sys.argv[1]))
