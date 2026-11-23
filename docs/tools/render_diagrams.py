from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from html import escape
import math

OUT=Path(__file__).resolve().parents[1]/"diagrams"
INK='#19334c'; BLUE='#245e9b'; LIGHT='#edf5fc'; GREY='#526273'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

class Canvas:
    def __init__(self,w,h,title):
        self.w=w; self.h=h; self.im=Image.new('RGB',(w*2,h*2),'white'); self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/>']
        self.text(w/2,43,title,32,True)
    def line(self,pts,color=INK,width=2,arrow=False):
        self.d.line([(int(x*2),int(y*2)) for x,y in pts],fill=color,width=width*2)
        self.svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
        if arrow:
            (x0,y0),(x,y)=pts[-2:]; a=math.atan2(y-y0,x-x0)
            p=[(x,y),(x-13*math.cos(a-.42),y-13*math.sin(a-.42)),(x-13*math.cos(a+.42),y-13*math.sin(a+.42))]
            self.poly(p,color,color,1)
    def poly(self,pts,fill='white',stroke=INK,width=2):
        p=[(round(x*2),round(y*2)) for x,y in pts]; self.d.polygon(p,fill=fill)
        self.d.line(p+[p[0]],fill=stroke,width=width*2)
        self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def rect(self,x,y,w,h,r=0,fill='white',stroke=INK,width=2):
        self.d.rounded_rectangle((x*2,y*2,(x+w)*2,(y+h)*2),radius=r*2,fill=fill,outline=stroke,width=width*2)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def ellipse(self,x,y,w,h,width=2):
        self.d.ellipse((x*2,y*2,(x+w)*2,(y+h)*2),fill='white',outline=INK,width=width*2)
        self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="white" stroke="{INK}" stroke-width="{width}"/>')
    def text(self,x,y,s,size=23,bold=False,color=INK,bg=False,under=False):
        font=ImageFont.truetype(BOLD if bold else FONT,size*2); lines=s.split('\n'); step=size*1.28
        for i,t in enumerate(lines):
            yy=y+(i-(len(lines)-1)/2)*step
            box=self.d.textbbox((x*2,yy*2),t,font=font,anchor='mm')
            if bg:
                self.d.rectangle((box[0]-7,box[1]-6,box[2]+7,box[3]+6),fill='white')
                self.svg.append(f'<rect x="{box[0]/2-4}" y="{box[1]/2-3}" width="{(box[2]-box[0])/2+8}" height="{(box[3]-box[1])/2+6}" fill="white"/>')
            self.d.text((x*2,yy*2),t,font=font,anchor='mm',fill=color)
            self.svg.append(f'<text x="{x}" y="{yy}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="middle" dominant-baseline="central"'+(' text-decoration="underline"' if under else '')+'>'+escape(t)+'</text>')
            if under:self.d.line((box[0],box[3]+3,box[2],box[3]+3),fill=color,width=2)
    def entity(self,x,y,w,h,label):
        self.rect(x,y,w,h,fill=LIGHT,stroke=BLUE);self.text(x+w/2,y+h/2,label,24,True)
    def diamond(self,cx,cy,w,h,label='',size=22):
        self.poly([(cx,cy-h/2),(cx+w/2,cy),(cx,cy+h/2),(cx-w/2,cy)])
        if label:self.text(cx,cy,label,size)
    def attribute(self,cx,cy,w,label,connect,key=False):
        self.line([connect,(cx,cy)]);self.ellipse(cx-w/2,cy-27,w,54);self.text(cx,cy,label,20,under=key)
    def store(self,x,y,w,label,id):
        self.line([(x+w,y),(x,y),(x,y+64),(x+w,y+64)])
        self.line([(x+62,y),(x+62,y+64)]);self.text(x+31,y+32,id,22,True);self.text(x+62+(w-62)/2,y+32,label,22)
    def process(self,x,y,w,label,id):
        self.rect(x,y,w,140,r=16,fill=LIGHT,stroke=BLUE);self.line([(x,y+36),(x+w,y+36)],BLUE)
        self.text(x+w/2,y+18,id,21,True);self.text(x+w/2,y+88,label,25)
    def save(self,name):
        self.im.resize((self.w,self.h),Image.Resampling.LANCZOS).save(OUT/(name+'.png'))
        (OUT/(name+'.svg')).write_text('\n'.join(self.svg+['</svg>']),encoding='utf-8')

def chen():
    c=Canvas(1600,1540,'Информационная модель — Чен')
    # Relationships, with maximum cardinalities. Optional participation is specified in the document.
    c.line([(390,255),(650,255)]);c.line([(870,255),(1120,255)])
    c.diamond(760,255,220,108,'содержит');c.text(470,235,'1');c.text(1030,235,'N')
    c.line([(245,300),(245,428)]);c.line([(245,532),(245,680)])
    c.diamond(245,480,210,104,'регистрирует',20);c.text(265,350,'1');c.text(265,625,'N')
    c.line([(1300,300),(1300,428)]);c.line([(1300,532),(1300,680)])
    c.diamond(1300,480,210,104,'включает');c.text(1325,350,'M');c.text(1325,625,'N')
    c.line([(390,700),(530,700),(530,480),(650,480)])
    c.line([(870,480),(1010,480),(1010,280),(1120,280)])
    c.diamond(760,480,220,108,'использует');c.text(455,678,'N');c.text(1060,308,'1')
    c.line([(245,770),(245,908)]);c.line([(245,1012),(245,1160)])
    c.diamond(245,960,210,104,'дает');c.text(268,805,'1');c.text(268,1110,'1')
    c.line([(1300,770),(1300,908)]);c.line([(1300,1012),(1300,1160)])
    c.diamond(1300,960,210,104,'входит в');c.text(1325,805,'M');c.text(1325,1110,'N')
    c.line([(390,1205),(650,1205)]);c.line([(870,1205),(1120,1205)])
    c.diamond(760,1205,220,108,'содержит');c.text(470,1183,'1');c.text(1030,1183,'N')
    # Attributes use ellipses; record identifiers are underlined.
    c.attribute(150,145,180,'experimentId',(180,210),True);c.attribute(420,145,210,'название',(350,210))
    c.attribute(1150,145,200,'snapshotId',(1200,210),True);c.attribute(1440,145,190,'версия',(1420,210))
    c.attribute(110,850,170,'runId',(150,770),True);c.attribute(445,850,270,'конфигурация',(360,770))
    c.attribute(1090,850,190,'valueId',(1180,770),True);c.attribute(1465,850,225,'представление',(1420,770))
    c.attribute(110,1330,185,'resultId',(150,1250),True);c.attribute(445,1330,270,'содержимое',(360,1250))
    c.attribute(1110,1330,190,'clusterId',(1180,1250),True);c.attribute(1430,1330,210,'номер',(1420,1250))
    for x,y,w,t in [(100,210,290,'Эксперимент'),(1120,210,360,'Снимок набора'),(100,680,290,'Запуск'),(1120,680,360,'Запись величины'),(100,1160,290,'Результат'),(1120,1160,360,'Кластер')]:c.entity(x,y,w,90,t)
    c.text(800,1435,'Прямоугольник — сущность; ромб — связь; овал — атрибут; подчеркнуто — ключ.',20)
    c.text(800,1474,'1 / M / N — максимальная кратность. Обязательность и ограничения — в описании данных.',20,color=GREY)
    c.save('01-chen')

def dfd():
    c=Canvas(1800,2240,'Функции и потоки данных — Гейн–Сарсон')
    rows=[
      ('1.0','Задать и изменить\nнечеткие величины','параметры / правки','величины / ошибки','текущее\nсостояние','обновленные\nвеличины'),
      ('2.0','Сгенерировать\nчисла или набор','режим / диапазоны\nчисло N / seed','выборка или набор\nошибки','параметры\nвеличины','данные и\nконтекст PRNG'),
      ('3.0','Принадлежность,\nарифметика и сравнение','операция / операнды\nx / уровень α','μ / сечение / ранг\nрезультат / ошибки','операнды /\nнастройки','результат\nзапуска'),
      ('4.0','Кластеризовать\nнабор','набор / критерий\nα / число групп K','кластеры / история\nстатус','снимок /\nнастройки','результат\nкластеризации'),
      ('5.0','Сохранить, загрузить\nили экспортировать','действие / путь\nформат','данные / подтверждение\nошибки','снимок\nэксперимента','восстановленное\nсостояние')]
    for i,(id,name,inp,out,read,write) in enumerate(rows):
        y=130+i*320
        c.rect(45,y+64,255,110);c.text(172,y+91,'E1',20,True);c.text(172,y+135,'Потребитель',24)
        c.process(650,y+48,400,name,id)
        c.store(1330,y+46,410,'Эксперимент','D1')
        c.store(1330,y+217,410,'Журнал','D2')
        c.line([(300,y+93),(650,y+93)],arrow=True);c.text(475,y+60,inp,21,bg=True)
        c.line([(650,y+157),(300,y+157)],arrow=True);c.text(475,y+200,out,21,bg=True)
        c.line([(1330,y+63),(1050,y+63)],arrow=True);c.text(1190,y+26,read,20,bg=True)
        c.line([(1050,y+140),(1200,y+140),(1200,y+95),(1330,y+95)],arrow=True);c.text(1190,y+176,write,20,bg=True)
        c.line([(850,y+188),(850,y+249),(1330,y+249)],arrow=True);c.text(1080,y+228,'запись: входы, исход, значения',20,bg=True)
        if i==4:
            c.store(1330,y+334,410,'Файлы JSON / CSV','D3')
            c.line([(740,y+188),(740,y+354),(1330,y+354)],arrow=True);c.text(1060,y+330,'JSON / CSV для записи',20,bg=True)
            c.line([(1330,y+383),(680,y+383),(680,y+188)],arrow=True);c.text(1060,y+407,'JSON для загрузки',20,bg=True)
    y=1860
    c.rect(45,y+64,255,110);c.text(172,y+91,'E1',20,True);c.text(172,y+135,'Потребитель',24)
    c.process(650,y+48,400,'Прочитать журнал','6.0');c.store(1330,y+46,410,'Журнал','D2')
    c.line([(300,y+93),(650,y+93)],arrow=True);c.text(475,y+60,'период / фильтры',21,bg=True)
    c.line([(650,y+157),(300,y+157)],arrow=True);c.text(475,y+200,'записи / ошибки',21,bg=True)
    c.line([(1330,y+78),(1050,y+78)],arrow=True);c.text(1190,y+46,'записи журнала',20,bg=True)
    c.text(900,2160,'E1 — JavaFX или Java-клиент. D1 — состояние в памяти; D2 и D3 — файлы.',21)
    c.text(900,2196,'Повторы E1, D1 и D2 обозначают те же объекты. Стрелки передают данные, а не порядок шагов.',20,color=GREY)
    c.save('02-gane-sarson')

def c4():
    c=Canvas(1500,1440,'Компоненты приложения — C4 C3')
    c.rect(590,125,320,75,fill='#f2f3f5')
    c.text(750,150,'Пользователь',24,True)
    c.text(750,179,'[Person]',18,color=GREY)
    c.rect(40,255,1420,1035,stroke=BLUE)
    c.text(300,290,'Student Lab Desktop\n[Container: Java / JavaFX, одна JVM]',21,True)
    def box(x,y,w,h,title,tech,body):
        c.rect(x,y,w,h,r=7,fill=LIGHT,stroke=BLUE)
        c.text(x+w/2,y+29,title,22,True)
        c.text(x+w/2,y+61,tech,19,color=GREY)
        c.text(x+w/2,y+110,body,22)
    box(520,330,460,150,'К1 Интерфейс','[Component: JavaFX / MVVM]',
        'Ввод, графики, фоновые задачи')
    box(520,615,460,170,'К2 Прикладные сценарии','[Component: Java]',
        'Эксперимент, снимки, запуски\nПорты хранения и журнала')
    box(80,1000,390,170,'К3 Алгоритмы','[Component: Java]',
        'Генерация, арифметика\nСравнение, кластеризация')
    box(540,1000,420,170,'К4 Математическая модель','[Component: Java]',
        'Нечёткие величины\nИнтервалы и α-сечения')
    box(1020,615,400,170,'К5 Файловые адаптеры','[Component: Java]',
        'JSON, CSV, журнал\nРеализации портов К2')
    c.line([(750,200),(750,330)],arrow=True)
    c.text(890,228,'Работает через GUI',19,bg=True)
    c.line([(750,480),(750,615)],arrow=True)
    c.text(750,546,'Вызывает сценарии',21,bg=True)
    c.line([(520,685),(275,685),(275,1000)],arrow=True)
    c.text(298,845,'Запускает\nвычисления',21,bg=True)
    c.line([(750,785),(750,1000)],arrow=True)
    c.text(750,887,'Использует модель',21,bg=True)
    c.line([(980,725),(1020,725)],arrow=True)
    c.text(1175,832,'Вызывает через порты\nExperimentStore / ResultExporter\nOperationLog / OperationLogReader',18,bg=True)
    c.line([(470,1090),(540,1090)],arrow=True)
    c.text(505,1225,'К3 использует контракт FuzzyNumber из К4',19)
    c.text(750,1333,'Стрелки — основные обращения во время работы; внутренние вызовы — Java API.',21)
    c.text(750,1371,'Зависимости сборки приведены отдельно: К2 зависит от своих портов, К5 реализует их.',20,color=GREY)
    c.text(750,1405,'К1 связывает реализации при запуске. Модуль Gradle здесь не является отдельным контейнером.',19,color=GREY)
    c.save('04-c4-components')

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    chen();dfd();c4()
    print('Created Chen, DFD and C4 diagrams.')

