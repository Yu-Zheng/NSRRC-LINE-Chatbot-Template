from linebot.models import (
    MessageTemplateAction, CarouselTemplate,CarouselColumn
)
from epics import caget

global Webhook_URL
Webhook_URL=''

#===========================================
#FE Tempture Carousel
#===========================================
def FE_Temp_Actions(First, Second, Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='Temp Status FE%s'%First),
             MessageTemplateAction(label='FE%s'%Second,text='Temp Status FE%s'%Second),
             MessageTemplateAction(label='FE%s'%Third,text='Temp Status FE%s'%Third)]
    return actions

def FE_Temp_Carousel():
    Image='%s/static/FE_Device_Temp.jpg'%Webhook_URL
    template=CarouselTemplate(
                              columns=[CarouselColumn(thumbnail_image_url=Image,title='TPS FE Tempture Status',text='FE05 - FE21',actions=FE_Temp_Actions('05','09','21')),
                                       CarouselColumn(thumbnail_image_url=Image,title='TPS FE Tempture Status',text='FE23 - FE41',actions=FE_Temp_Actions('23','25','41')),
                                       CarouselColumn(thumbnail_image_url=Image,title='TPS FE Tempture Status',text='FE45',actions=[MessageTemplateAction(label='FE45',text='Temp Status FE45'),
                                                                                                                                 MessageTemplateAction(label='None',text='None'),
                                                                                                                                 MessageTemplateAction(label='None',text='None')])
                                       ]
                              )
    return template

#===========================================
#FE Vacuum Carousel
#===========================================
def FE_Vacuum_Actions(First, Second, Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='Vacuum Status FE%s'%First),
             MessageTemplateAction(label='FE%s'%Second,text='Vacuum Status FE%s'%Second),
             MessageTemplateAction(label='FE%s'%Third,text='Vacuum Status FE%s'%Third)]
    return actions

def FE_Vacuum_Carousel():
    Image='%s/static/Vacuum.jpg'%Webhook_URL
    template=CarouselTemplate(
        columns=[CarouselColumn(thumbnail_image_url=Image,title='TPS FE Vacuum Status',text='FE05 - FE21',actions=FE_Vacuum_Actions('05','09','21')),
                 CarouselColumn(thumbnail_image_url=Image,title='TPS FE Vacuum Status',text='FE23 - FE41',actions=FE_Vacuum_Actions('23','25','41')),
                 CarouselColumn(thumbnail_image_url=Image,title='TPS FE Vacuum Status',text='FE45',actions=[MessageTemplateAction(label='FE45',text='Vacuum Status FE45'),
                                                                                                                                MessageTemplateAction(label='None',text='None'),
                                                                                                                                MessageTemplateAction(label='None',text='None')])
                ]
    )
    return template
#===========================================
#FE Valve Carousel
#===========================================
def FE_Valve_Actions(First, Second, Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='Valve Status FE%s'%First),
             MessageTemplateAction(label='FE%s'%Second,text='Valve Status FE%s'%Second),
             MessageTemplateAction(label='FE%s'%Third,text='Valve Status FE%s'%Third)]
    return actions

def FE_Valve_Carousel():
    Image='%s/static/FE_Valve.jpg'%Webhook_URL
    template=CarouselTemplate(
        columns=[CarouselColumn(thumbnail_image_url=Image,title='TPS FE Valve Status',text='FE05 - FE21',actions=FE_Valve_Actions('05','09','21')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS FE Valve Status',text='FE23 - FE41',actions=FE_Valve_Actions('23','25','41')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS FE Valve Status',text='FE45',actions=[MessageTemplateAction(label='FE45',text='Valve Status FE45'),
                                                                                                                                 MessageTemplateAction(label='None',text='None'),
                                                                                                                                 MessageTemplateAction(label='None',text='None')])
                 ]
    )
    return template
#===========================================
#ID Carousel
#===========================================
def ID_Actions(First, Second, Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='ID Gap FE%s'%First),
             MessageTemplateAction(label='FE%s'%Second,text='ID Gap FE%s'%Second),
             MessageTemplateAction(label='FE%s'%Third,text='ID Gap FE%s'%Third)]
    return actions

def ID_Gap_Carousel():
    Image='%s/static/ID.jpg'%Webhook_URL
    template=CarouselTemplate(
        columns=[CarouselColumn(thumbnail_image_url=Image,title='TPS ID Gap Status',text='FE05 - FE21',actions=ID_Actions('05','09','21')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS ID Gap Status',text='FE23 - FE41',actions=ID_Actions('23','25','41')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS ID Gap Status',text='FE45',actions=[MessageTemplateAction(label='FE45',text='ID Gap FE45'),
                                                                                                    MessageTemplateAction(label='None',text='None'),
                                                                                                    MessageTemplateAction(label='None',text='None')])
                ]
    )
    return template

def ID_Gap_Result(FE_number):
    ID_Dict={
        "05":["TPS:05A:getGap"],
        "09":["TPS:09AD:getGap","TPS:09AU:getGap"],
        "21":["TPS:21A:getGap"],
        "23":["TPS:23A:getGap"],
        "25":["TPS:25AD:getGap","TPS:25AU:getGap"],
        "41":["TPS:41AD:getGap","TPS:41AD:getPhase","TPS:41AU:getGap","TPS:41AU:getPhase","TPS:41PS:getGap"],
        "45":["TPS:45A:getGap","TPS:45A:getPhase"]
    }
    Result=""
    for i in ID_Dict[FE_number]:
        Temp=caget(i)
        Result=Result+i+"=>\n"+('%.6f'%Temp)+"\n\n"
        print(i+"=>"+str(Temp))
    Result=Result.rstrip('\n\n')
    return Result

#===========================================
#Interlock Carousel
#===========================================
def Interlock_Actions(First, Second,Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='Interlock Alarm FE%s'%First),
            MessageTemplateAction(label='FE%s'%Second,text='Interlock Alarm FE%s'%Second),
            MessageTemplateAction(label='FE%s'%Third,text='Interlock Alarm FE%s'%Third)]
    return actions
def Interlock_Carousel():
    Image='%s/static/Interlock.jpg'%Webhook_URL
    template=CarouselTemplate(
        columns=[CarouselColumn(thumbnail_image_url=Image,title='TPS Interlock Status',text='FE05 - FE21',
                    actions=Interlock_Actions('02','05','09')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS Interlock Status',text='FE23 - FE25',
                    actions=Interlock_Actions('21','23','25')),
                CarouselColumn(thumbnail_image_url=Image,title='TPS Interlock Status',text='FE41 - FE45',
                    actions=Interlock_Actions('41','44','45'))
                ]
        )
    return template
#===========================================
#XBPM Carousel
#===========================================
def XBPM_Actions(First, Second, Third):
    actions=[MessageTemplateAction(label='FE%s'%First,text='XBPM FE%s'%First),
            MessageTemplateAction(label='FE%s'%Second,text='XBPM FE%s'%Second),
            MessageTemplateAction(label='FE%s'%Third,text='XBPM FE%s'%Third)]
    return actions

def XBPM_Carousel():
    Image='%s/static/XBPM.jpg'%Webhook_URL
    template=CarouselTemplate(
        columns=[
            CarouselColumn(thumbnail_image_url=Image,title='TPS FE XBPM',text='FE05 - FE21',
                actions=XBPM_Actions('05','09','21')),
            CarouselColumn(thumbnail_image_url=Image,title='TPS FE XBPM',text='FE23 - FE41',
                actions=XBPM_Actions('23','25','41'))
        ]
    )
    return template
#============================================
