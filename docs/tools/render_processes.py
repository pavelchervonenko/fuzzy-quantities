"""Generate six descriptive BPMN models, PNG/SVG views and BPMN XML with DI.

Run beside render_diagrams.py. No BPMN engine or Java code is generated.
"""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from render_diagrams import Canvas, OUT, LIGHT, BLUE, GREY
from render_diagrams import FONT
from PIL import ImageFont

MODELS = [
 dict(id='1', slug='values', title='Задать и изменить величины',
      prepare='Получить параметры и текущий снимок\nПроверить c, s, k, ε и численные границы',
      work='Создать неизменяемую величину\nи опубликовать новый снимок',
      success='Подготовить ответ:\nвеличина и новый снимок', cancel=False, log=True),
 dict(id='2', slug='generation', title='Сгенерировать набор или выборку',
      prepare='Проверить режим, N, диапазоны и seed\nЗафиксировать конфигурацию генерации',
      choices=[('нечёткие величины','Генерировать c и s\nПостроить N величин\nс общими k и ε'),
               ('числовая выборка','Генерировать независимые Z\nВычислить N чисел Стьюдента\nε не применяется')],
      success='Подготовить набор или выборку\nи параметры воспроизведения',cancel=True,log=True),
 dict(id='3', slug='operations', title='Исследовать и выполнить операции',
      prepare='Зафиксировать операнды и действие\nПроверить входы и допустимость деления',
      choices=[('принадлежность / сечение','Вычислить μ(x)\nили α-сечение'),
               ('арифметика','Вычислить +, −, × или ÷\nна общей сетке α\nПроверить итоговые сечения'),
               ('сравнение','Вычислить ранги\nна общей сетке α\nСравнить ранги')],
      success='Подготовить значение, сечение,\nтабличную величину или сравнение',cancel=True,log=True),
 dict(id='4', slug='clustering', title='Кластеризовать набор',
      prepare='Зафиксировать снимок, критерий, α и K\nПроверить набор и настройки',
      work='Получить сечения и расстояния\nОбъединять ближайшие группы до K\nПроверить разбиение; учитывать отмену',
      success='Подготовить разбиение\nи привязку к снимку',cancel=True,log=True),
 dict(id='5', slug='files', title='Сохранить, загрузить или экспортировать',
      prepare='Проверить действие, путь и формат\nЗафиксировать данные для записи',
      choices=[('сохранить','Сериализовать эксперимент\nЗаписать временный файл\nАтомарно заменить целевой'),
               ('загрузить','Прочитать и проверить JSON\nПостроить кандидат состояния\nПрименить целиком'),
               ('экспортировать','Подготовить CSV результата\nЗаписать временный файл\nАтомарно заменить целевой')],
      success='Подготовить подтверждение\nили загруженный эксперимент',cancel=False,log=True),
 dict(id='6', slug='journal', title='Прочитать журнал',
      prepare='Проверить период и фильтры\nВыбрать источник журнала',
      work='Зафиксировать границу чтения\nПрочитать полные записи\nПрименить фильтры',
      success='Подготовить список записей\nПустой список допустим',cancel=False,log=False)
]

NS = {'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL',
      'bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI',
      'dc':'http://www.omg.org/spec/DD/20100524/DC',
      'di':'http://www.omg.org/spec/DD/20100524/DI',
      'xsi':'http://www.w3.org/2001/XMLSchema-instance'}
for k,v in NS.items(): ET.register_namespace(k,v)
def tag(ns,name): return '{'+NS[ns]+'}'+name

def model(spec):
    branched=bool(spec.get('choices'))
    status_y=1190 if branched else 960
    result_y=status_y+165
    merge_y=result_y+230
    log_y=merge_y+100
    return_y=log_y+155 if spec['log'] else log_y
    end_y=return_y+170
    g=dict(id=spec['id'],title=spec['title'],slug=spec['slug'],width=1600,height=end_y+200,nodes=[],flows=[])
    def node(id,kind,x,y,w,h,text='',label=None):
        g['nodes'].append(dict(id=id,kind=kind,x=x,y=y,w=w,h=h,text=text,label=label))
    def flow(src,dst,pts,label='',at=None):
        g['flows'].append(dict(id='f'+str(len(g['flows'])+1),src=src,dst=dst,pts=pts,label=label,at=at))
    def task(id,x,y,w,text): node(id,'task',x,y,w,120,text)
    def gate(id,x,y,name='',label=None): node(id,'exclusiveGateway',x-40,y-40,80,80,name,label)
    node('start','startEvent',778,190,44,44,'Запрос получен',[945,212])
    task('prepare',500,280,600,spec['prepare'])
    flow('start','prepare',[(800,234),(800,280)])
    gate('valid',800,490,'Входы допустимы?',[1030,455])
    flow('prepare','valid',[(800,400),(800,450)])
    gate('status',800,status_y,'Исход выполнения',[1030,status_y-45])
    if branched:
        gate('mode',800,650,'Выбранное действие',[1030,605])
        flow('valid','mode',[(800,530),(800,610)],'да',[835,565])
        xs=[320,1280] if len(spec['choices'])==2 else [320,800,1280]
        gate('choice_merge',800,1050)
        for i,((name,body),x) in enumerate(zip(spec['choices'],xs)):
            n='work'+str(i+1);task(n,x-205,790,410,body)
            if x<800:
                pts=[(760,650),(x,650),(x,790)];at=[530,625]
                out=[(x,910),(x,1050),(760,1050)]
            elif x>800:
                pts=[(840,650),(x,650),(x,790)];at=[1060,690]
                out=[(x,910),(x,1050),(840,1050)]
            else:
                pts=[(800,690),(800,790)];at=[800,740]
                out=[(800,910),(800,1010)]
            flow('mode',n,pts,name,at);flow(n,'choice_merge',out)
        flow('choice_merge','status',[(800,1090),(800,status_y-40)])
    else:
        task('work',500,650,600,spec['work'])
        flow('valid','work',[(800,530),(800,650)],'да',[835,585])
        flow('work','status',[(800,770),(800,status_y-40)])
    task('success',115,result_y,410,spec['success'])
    task('failure',1075,result_y,410,'Подготовить ошибку\nбез успешного результата')
    # Invalid input and computation failure are alternative routes, never concurrent.
    flow('valid','failure',[(840,490),(1530,490),(1530,result_y+60),(1485,result_y+60)],'нет',[1430,465])
    flow('status','success',[(760,status_y),(320,status_y),(320,result_y)],'успех',[540,status_y-25])
    flow('status','failure',[(840,status_y),(1280,status_y),(1280,result_y)],'ошибка',[1070,status_y+35])
    gate('outcome_merge',800,merge_y)
    flow('success','outcome_merge',[(320,result_y+120),(320,merge_y),(760,merge_y)])
    flow('failure','outcome_merge',[(1280,result_y+120),(1280,merge_y),(840,merge_y)])
    if spec['cancel']:
        task('cancel',595,result_y,410,'Подготовить ответ об отмене\nОтбросить незавершённые данные')
        flow('status','cancel',[(800,status_y+40),(800,result_y)],'отмена',[845,status_y+100])
        flow('cancel','outcome_merge',[(800,result_y+120),(800,merge_y-40)])
    if spec['log']:
        task('log',500,log_y,600,'Записать входы, исход и значения в журнал\nПри сбое добавить предупреждение')
        flow('outcome_merge','log',[(800,merge_y+40),(800,log_y)])
        flow('log','return',[(800,log_y+120),(800,return_y)])
    else:
        flow('outcome_merge','return',[(800,merge_y+40),(800,return_y)])
    task('return',500,return_y,600,'Вернуть ответ потребителю')
    node('end','endEvent',778,end_y,44,44,'Запрос завершён',[960,end_y+22])
    flow('return','end',[(800,return_y+120),(800,end_y)])
    return g

def render(g,spec):
    c=Canvas(g['width'],g['height'],f"{g['id']}.0 {g['title']}")
    c.rect(45,120,1510,g['height']-250)
    c.rect(45,120,1510,42,fill=LIGHT)
    c.text(800,141,'Student Lab: обработка запроса приложением',22,True)
    for f in g['flows']: c.line(f['pts'],arrow=True)
    for n in g['nodes']:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];cx=x+w/2;cy=y+h/2
        if n['kind']=='task':
            size=21 if w<500 else 22
            while max(ImageFont.truetype(FONT,size).getlength(t) for t in n['text'].split('\n'))>w-30:
                size-=1
            assert size>=17, (n['id'],n['text'])
            c.rect(x,y,w,h,r=16);c.text(cx,cy,n['text'],size)
        elif n['kind']=='exclusiveGateway': c.diamond(cx,cy,w,h,'×',34)
        else: c.ellipse(x,y,w,h,width=5 if n['kind']=='endEvent' else 2)
        if n.get('label'):c.text(*n['label'],n['text'],20,bg=True)
    for f in g['flows']:
        if f['label']:c.text(*f['at'],f['label'],19,bg=True)
    note='Отмена проверяется внутри вычислений; изменения публикуются только после успешного завершения.'
    if not spec['cancel']:note='Недопустимые входы и ошибки выполнения возвращаются как разные коды ошибки.'
    if not spec['log']:note='Чтение журнала не записывает само себя; ошибки чтения возвращаются напрямую в GUI / API.'
    c.text(800,g['height']-75,'Круг — событие; скруглённый блок — задача; ромб × — исключающий шлюз.',20)
    c.text(800,g['height']-40,note,19,color=GREY)
    c.save('bpmn-'+g['id']+'0-'+g['slug'])

def xml(g):
    ident='P'+g['id'];pid=ident+'_process';coll=ident+'_collaboration';part=ident+'_participant'
    root=ET.Element(tag('bpmn','definitions'),id=ident+'_definitions',targetNamespace='https://student-lab.local/design',
                    exporter='Student Lab design tools')
    co=ET.SubElement(root,tag('bpmn','collaboration'),id=coll)
    ET.SubElement(co,tag('bpmn','participant'),id=part,name='Student Lab',processRef=pid)
    proc=ET.SubElement(root,tag('bpmn','process'),id=pid,name=g['title'],isExecutable='false')
    ET.SubElement(proc,tag('bpmn','documentation')).text='Descriptive model; see docs/processes.md for contracts and handled outcomes.'
    for n in g['nodes']:
        attrs={'id':ident+'_'+n['id'],'name':n['text'].replace('\n',' ')}
        if n['kind']=='exclusiveGateway':
            outgoing=sum(f['src']==n['id'] for f in g['flows'])
            attrs['gatewayDirection']='Diverging' if outgoing>1 else 'Converging'
        e=ET.SubElement(proc,tag('bpmn',n['kind']),attrs)
        for f in g['flows']:
            if f['dst']==n['id']:ET.SubElement(e,tag('bpmn','incoming')).text=ident+'_'+f['id']
            if f['src']==n['id']:ET.SubElement(e,tag('bpmn','outgoing')).text=ident+'_'+f['id']
    for f in g['flows']:
        ET.SubElement(proc,tag('bpmn','sequenceFlow'),id=ident+'_'+f['id'],name=f['label'],
                      sourceRef=ident+'_'+f['src'],targetRef=ident+'_'+f['dst'])
    diag=ET.SubElement(root,tag('bpmndi','BPMNDiagram'),id=ident+'_diagram')
    plane=ET.SubElement(diag,tag('bpmndi','BPMNPlane'),id=ident+'_plane',bpmnElement=coll)
    shape=ET.SubElement(plane,tag('bpmndi','BPMNShape'),id=part+'_di',bpmnElement=part,isHorizontal='false')
    ET.SubElement(shape,tag('dc','Bounds'),x='45',y='120',width='1510',height=str(g['height']-250))
    for n in g['nodes']:
        attrs={'id':ident+'_'+n['id']+'_di','bpmnElement':ident+'_'+n['id']}
        if n['kind']=='exclusiveGateway':attrs['isMarkerVisible']='true'
        shape=ET.SubElement(plane,tag('bpmndi','BPMNShape'),attrs)
        ET.SubElement(shape,tag('dc','Bounds'),dict(x=str(n['x']),y=str(n['y']),width=str(n['w']),height=str(n['h'])))
        if n.get('label'):
            label=ET.SubElement(shape,tag('bpmndi','BPMNLabel'))
            ET.SubElement(label,tag('dc','Bounds'),x=str(n['label'][0]-140),y=str(n['label'][1]-14),width='280',height='28')
    for f in g['flows']:
        edge=ET.SubElement(plane,tag('bpmndi','BPMNEdge'),id=ident+'_'+f['id']+'_di',bpmnElement=ident+'_'+f['id'])
        for x,y in f['pts']:ET.SubElement(edge,tag('di','waypoint'),x=str(x),y=str(y))
        if f['at']:
            label=ET.SubElement(edge,tag('bpmndi','BPMNLabel'))
            ET.SubElement(label,tag('dc','Bounds'),x=str(f['at'][0]-160),y=str(f['at'][1]-14),width='320',height='28')
    ET.indent(root)
    ET.ElementTree(root).write(OUT/('bpmn-'+g['id']+'0-'+g['slug']+'.bpmn'),encoding='utf-8',xml_declaration=True)

def validate(g):
    ids={n['id'] for n in g['nodes']};assert len(ids)==len(g['nodes'])
    for f in g['flows']:assert f['src'] in ids and f['dst'] in ids
    def reachable(start,reverse=False):
        seen={start};q=[start]
        while q:
            a=q.pop()
            for f in g['flows']:
                src,dst=(f['dst'],f['src']) if reverse else (f['src'],f['dst'])
                if src==a and dst not in seen:seen.add(dst);q.append(dst)
        return seen
    assert reachable('start')==ids and reachable('end',True)==ids
    for n in g['nodes']:
        incoming=[f for f in g['flows'] if f['dst']==n['id']]
        outgoing=[f for f in g['flows'] if f['src']==n['id']]
        assert incoming or n['kind']=='startEvent'
        assert outgoing or n['kind']=='endEvent'
        if n['kind']=='exclusiveGateway' and len(outgoing)>1:
            assert all(f['label'] for f in outgoing)
    # All shapes remain inside the participant (except the participant title itself).
    assert all(n['x']>=45 and n['x']+n['w']<=1555 and n['y']>=162 and n['y']+n['h']<g['height']-130 for n in g['nodes'])

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    graphs=[]
    for spec in MODELS:
        g=model(spec);validate(g);render(g,spec);xml(g);graphs.append(g)
    (OUT/'process-models.json').write_text(json.dumps(graphs,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Six BPMN models generated; graph references, reachability and gateway labels checked.')
