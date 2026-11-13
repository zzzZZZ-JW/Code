from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
root=Path(__file__).resolve().parent
materials=Path.home()/'Library/CloudStorage/OneDrive-个人/资料/人工智能专业导论'
artifacts=materials/'.codex-lab3'
src=materials/'10.16/2506456010-张佳伟-2506456052.docx'
out=src.with_name('2506456010-张佳伟-实验三-完成版.docx')
d=Document(src); original=list(d.paragraphs)
# Retain section breaks and original text, while allowing continuous flow.
for i,p in enumerate(original):
 if i>=4:
  f=p.paragraph_format; f.space_before=Pt(0); f.space_after=Pt(3)
  f.line_spacing=1.15; f.keep_with_next=False; f.page_break_before=False
for i in (4,10,16,22,25):
 original[i].paragraph_format.keep_with_next=True
for i in (9,20,21,27):
 p=original[i]
 if not p._p.xpath('.//w:sectPr'): p._p.getparent().remove(p._p)
for i in (23,24,26): original[i]._p.getparent().remove(original[i]._p)
anchor=original[25]
def add(text='',kind='body'):
 p=anchor.insert_paragraph_before(text,style='Normal')
 pf=p.paragraph_format
 pf.space_before=Pt(0);pf.space_after=Pt(3);pf.line_spacing=1.15
 pf.first_line_indent=Pt(0);pf.left_indent=Pt(0);pf.right_indent=Pt(0)
 pf.keep_with_next=kind=='sub';pf.keep_together=False;pf.page_break_before=False
 for r in p.runs:
  r.font.name='Times New Roman';r.font.size=Pt(10.5)
  r._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'宋体')
  if kind=='sub':r.bold=True;r.font.size=Pt(11)
 return p
def code(text):
 for line in text.strip('\n').splitlines():
  
  if not line.strip(): continue
  p=add(line,'code');p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.0
  for r in p.runs:r.font.name='Courier New';r.font.size=Pt(9)
def pic(n,caption):
 p=add();p.paragraph_format.space_after=Pt(0)
 p.add_run().add_picture(str(artifacts/f'run-{n}.png'),width=Cm(12.0))
 p.paragraph_format.keep_with_next=True
 p=add(caption);p.alignment=1
 for r in p.runs:r.font.size=Pt(9)
add('1  实验环境与实现思路','sub')
add('本次使用 macOS arm64 环境及 Python 3.12.14 运行程序，仅使用标准库。三道题分别建立独立知识库，避免其他规则影响指定案例；截图为本地结果页面直接显示 Python 子进程的标准输出，包含断言检查结果和进程退出码。')
add('将原规则中的条件函数改为显式症状列表，用 all 判断所有条件是否满足，再用 min 取这些条件的最低置信度。沿用讲义中症状置信度大于 0.5 的触发阈值。症状事实与推荐结果分开存储，同一穴位仅保留更高置信度。Decimal 用于避免十进制乘积的浮点显示误差。')
add('2  三题共用的核心代码','sub')
add('以下为实际运行程序中的知识库类。每条规则保存“症状元组、结论穴位、规则置信度”，priority 参数控制是否优先执行高规则置信度规则。')
source=(root/'expert_system.py').read_text()
code('from decimal import Decimal\n\n'+source[source.index('class AcupunctureProductionSystem:'):source.index('\n\ndef make_system')])
add('3  第一题 置信度计算优化','sub')
add('原方法把每个症状单独传给条件函数。对于“头痛且牙痛”，单个症状无法满足整个合取条件，生成的置信度列表为空，min 会报错。修改后直接读取规则声明的全部症状：条件全部成立才计算 0.9 × min(0.8, 0.6) = 0.54。')
code('''aps = AcupunctureProductionSystem()
aps.add_fact("头痛", 0.8)
aps.add_fact("牙痛", 0.6)
aps.add_rule(["头痛", "牙痛"], "合谷", 0.9)
result = aps.run()
assert result == {"合谷": Decimal("0.54")}''')
pic(1,'图1  第一题实际输出及边界检查')
add('运行结果为合谷 0.540，与题目要求一致。缺少牙痛，或牙痛置信度恰好等于 0.5 时，条件均不成立，不生成推荐。该题单独测试合取规则；若同时保留“头痛→合谷 0.9”的单条件规则，其 0.72 会覆盖 0.54，因此不能用混合案例验证题设结果。')
add('4  第二题 添加风池推荐规则','sub')
add('复用修改后的 run 方法，将“鼻塞且流涕”写成两个必要条件，新增规则置信度 0.85。无需为新症状增加硬编码的排除列表。')
code('''aps = AcupunctureProductionSystem()
aps.add_fact("鼻塞", 0.8)
aps.add_fact("流涕", 0.7)
aps.add_rule(["鼻塞", "流涕"], "风池", 0.85)
result = aps.run()
assert result == {"风池": Decimal("0.595")}''')
pic(2,'图2  第二题实际输出及缺失条件检查')
add('计算得到 0.85 × min(0.8, 0.7) = 0.595，按两位小数显示为 0.60。缺少流涕时不触发规则，说明新规则正确表达了“且”的关系，而不是任意一个症状成立即可推荐。')
add('5  第三题 冲突消解与规则执行顺序','sub')
add('执行前用 sorted 按规则置信度降序排列，开启 priority=True 后，0.95 的胃痛规则先于 0.9 的头痛规则和 0.8 的便秘规则执行；置信度相同时保持原添加顺序。核心排序语句已包含在共用 run 方法中，对照测试代码如下。')
code('''def build_case():
    aps = AcupunctureProductionSystem()
    for name, value in [("头痛", 0.8), ("便秘", 0.7), ("胃痛", 0.9)]:
        aps.add_fact(name, value)
    aps.add_rule(["便秘"], "合谷", 0.8)
    aps.add_rule(["头痛"], "合谷", 0.9)
    aps.add_rule(["胃痛"], "足三里", 0.95)
    return aps
by_order = build_case().run()
by_priority = build_case().run(priority=True)
assert by_order == by_priority
assert by_priority == {"合谷": Decimal("0.72"),
                       "足三里": Decimal("0.855")}''')
pic(3,'图3  按添加顺序与按规则置信度降序执行的对照')
add('按添加顺序时，合谷先由便秘规则得到 0.56，再由头痛规则更新为 0.72；按优先级执行时，先输出足三里 0.855，再输出合谷 0.72，后续 0.56 不会覆盖较高结果。两种顺序的最终结果一致，排序改变的是触发先后。讲义中的“更高置信度才更新”机制已经避免最终结果被较低值锁定。')
add('规则置信度排序不等于最终推荐置信度排序，因为后者还受症状置信度影响。若需展示按最终得分排序的推荐列表，可另用 sorted(result.items(), key=lambda item: item[1], reverse=True)。本题按要求优先排序规则本身的置信度。')
# Insert summary after original heading by appending before a temporary anchor.
end=d.add_paragraph(); anchor=end
add('本次实验完成了多条件置信度计算、新规则扩展和冲突消解策略的实现。三个正常案例与三个边界、对照检查均通过，程序正常退出。前向推理从已知症状匹配规则，在结果没有进一步更新时停止。由于本实验的条件只引用输入症状，首轮得到推荐结果，下一轮确认无更新后结束。')
add('主要问题是原条件函数无法说明自己依赖哪些症状，逐个尝试症状会破坏合取语义。显式保存条件列表后，匹配与置信度计算使用同一组条件，代码也更容易扩展。将症状与结论分开存储，可以避免新增“牙痛”“鼻塞”等症状被误当作推荐穴位输出。')
add('通过执行顺序对照，我理解了规则优先级、结论置信度和结果合并策略的区别：优先执行高置信度规则决定处理顺序，取较大值决定同一结论如何合并。系统仍是采用给定规则的课程演示，置信度表示实验中的证据权重，不等同于临床疗效概率；若要支持多级推理，还需将结论作为后续规则可匹配的事实，并记录推理依据。')
end._p.getparent().remove(end._p)
for p in d.paragraphs[4:]:
    pr=p._p.get_or_add_pPr()
    snap=pr.find(qn('w:snapToGrid'))
    if snap is None:snap=OxmlElement('w:snapToGrid');pr.append(snap)
    snap.set(qn('w:val'),'false')
    spacing=pr.find(qn('w:spacing'))
    if spacing is not None:
        for a in ('beforeLines','afterLines','beforeAutospacing','afterAutospacing'):
            spacing.attrib.pop(qn('w:'+a),None)
    if not p._p.xpath('.//w:drawing'):
        p.paragraph_format.line_spacing=Pt(11.5 if p.runs and p.runs[0].font.name=='Courier New' else 14)

settings=d.settings.element
u=settings.find(qn('w:updateFields'))
if u is None:u=OxmlElement('w:updateFields');settings.append(u)
u.set(qn('w:val'),'true')
b=BytesIO();d.save(b)
allowed={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','word/settings.xml'}
with ZipFile(src) as old,ZipFile(b) as new,ZipFile(out,'w',ZIP_DEFLATED) as result:
 for n in old.namelist():result.writestr(n,new.read(n) if n in allowed else old.read(n))
 for n in new.namelist():
  if n not in old.namelist():result.writestr(n,new.read(n))
with ZipFile(src) as old,ZipFile(out) as new:
 for n in old.namelist():
  if n not in allowed:assert old.read(n)==new.read(n),n
assert all(p.text!='XXX' for p in Document(out).paragraphs)
print(out)
