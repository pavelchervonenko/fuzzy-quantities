"""Document/graph checks and numerical sanity checks of stated formulas."""
from pathlib import Path
import json, math, re
import xml.etree.ElementTree as ET
from PIL import Image
from render_processes import MODELS, model, validate, NS

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ok(name,details):checks.append(dict(check=name,status='passed',details=details))

graphs=json.loads((ROOT/'diagrams/process-models.json').read_text())
assert [g['id'] for g in graphs]==list('123456')
for g,spec in zip(graphs,MODELS):
    validate(g)
    assert json.dumps(g,sort_keys=True)==json.dumps(model(spec),sort_keys=True)
    xml=ET.parse(ROOT/'diagrams'/('bpmn-'+g['id']+'0-'+g['slug']+'.bpmn'))
    process=xml.find('.//bpmn:process',NS)
    assert process is not None and process.attrib['isExecutable']=='false'
    prefix='P'+g['id']+'_'
    nodes={e.attrib['id'] for e in process if e.tag.split('}')[-1] in ('task','exclusiveGateway','startEvent','endEvent')}
    assert nodes=={prefix+n['id'] for n in g['nodes']}
    flows={e.attrib['id']:e for e in process.findall('bpmn:sequenceFlow',NS)}
    assert len(flows)==len(g['flows'])
    for f in g['flows']:
        e=flows[prefix+f['id']]
        assert e.attrib['sourceRef']==prefix+f['src'] and e.attrib['targetRef']==prefix+f['dst']
        assert e.attrib['name']==f['label']
    allids=[e.attrib['id'] for e in xml.iter() if 'id' in e.attrib]
    assert len(allids)==len(set(allids))
    ids=set(allids)
    for e in xml.iter():
        for a in ('sourceRef','targetRef','processRef','bpmnElement'):
            if a in e.attrib:assert e.attrib[a] in ids
    assert len(xml.findall('.//bpmndi:BPMNEdge',NS))==len(flows)
    assert len(xml.findall('.//bpmndi:BPMNShape',NS))==len(nodes)+1
    for suffix in ('png','svg','bpmn'):assert (ROOT/'diagrams'/('bpmn-'+g['id']+'0-'+g['slug']+'.'+suffix)).exists()
ok('Six BPMN models','Coverage 1.0–6.0; graph reachability, conditions, XML references and DI checked. Not full BPMN XSD validation.')

count=0
for p in ROOT.glob('*.md'):
    for u in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' not in u and not u.startswith('#'):
            assert (p.parent/u).exists(),(str(p),u)
            count+=1
for p in (ROOT/'diagrams').glob('*.svg'):
    svg=ET.parse(p)
    labels=[''.join(e.itertext()) for e in svg.iter() if e.tag.endswith('}text')]
    for label in labels:
        assert not re.search(r'review-\d|V\d\s*/\s*M|\d{2}\.\d{2}\.\d{4}|·',label),(p,label)
for p in (ROOT/'diagrams').glob('*.png'):
    assert p.stat().st_size>0,('Empty PNG',p)
    with Image.open(p) as image:
        assert image.format=='PNG',(p,image.format)
        image.verify()
assert len(list((ROOT/'diagrams').glob('*.png')))==9
assert len(list((ROOT/'diagrams').glob('*.svg')))==9
assert len(list((ROOT/'diagrams').glob('*.bpmn')))==6
ok('Artifact structure',f'9 readable PNG, 9 SVG without service labels, 6 BPMN; {count} local links resolved.')

cases=0
for k in (1,5,10):
    for eps in (.001,.02):
        for c,s in ((0.,1.),(10.,1.),(-4.,2.5)):
            prior=None
            for alpha in (0.,.01,.1,.5,.9,1.):
                q=eps+(1-eps)*alpha
                r=s*math.sqrt(k*math.expm1(-2*math.log(q)/(k+1)))
                lo,hi=c-r,c+r
                if prior:assert prior[0]<=lo and hi<=prior[1]
                prior=lo,hi
                for x in (lo,hi):
                    mu=(1+(x-c)**2/(k*s*s))**(-(k+1)/2)
                    bounded=max(0,(mu-eps)/(1-eps))
                    assert math.isclose(bounded,alpha,abs_tol=2e-12)
                cases+=1
radius=math.sqrt(45)
assert math.isclose(radius,6.708203932499369)
ok('Alpha-cut formula sanity',f'{cases} parameter/level cases: boundary membership equals alpha, nesting holds; k=5 and epsilon=.001 support radius is sqrt(45)*s.')
ok('Scope','Checks concern design artifacts and formulas only; no Java application tests were run.')
report=dict(status='passed',checks=checks)
print(json.dumps(report,ensure_ascii=False,indent=2))
