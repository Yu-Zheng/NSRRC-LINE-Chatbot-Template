import re  # for number filter

from epics import caget
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent,
                            TemplateSendMessage, TextMessage, TextSendMessage)

from .Carousel import (FE_Temp_Carousel, FE_Vacuum_Carousel, FE_Valve_Carousel,
                       ID_Gap_Carousel, ID_Gap_Result, Interlock_Carousel,
                       XBPM_Carousel)
from .FE_Diagnosis import (FE_Diagnosis, FE_Temp, FE_VacPresure,
                           MP_FE_Diagnosis, Valve_Status)
from .XBPM_Query import XBPM_Status


def Rule_Based_Engine(event):
    str = event.message.text
    strupper = str.upper()
    # Help
    if "HELP" in strupper:
        Help_Result = TextSendMessage(text="目前可以使用：\n"
                                      "● 查詢TPS儲存環電流\n => TPS+Current\n\n"\
                                      #"● 查詢Front End狀態\n => FE+Status \n\n"\
                                      "● 查詢XBPM數值\n => XBPM+FE段數 \n\n"\
                                      "● 查詢前端區真空狀態\n => Vacuum+Status+FE段數\n\n"\
                                      "● Interlock功能:\n"\
                                      "----所有狀態----\n"\
                                      "=> Interlock+All\n"
                                      "----單站狀態----\n"\
                                      "=> Interlock+Status\n+FE段數\n"\
                                      "----警示點位----\n"\
                                      "=> Interlock+Alarm\n+FE段數")
        return Help_Result

    # Reply TPS Current
    if "TPS" in strupper and "CURRENT" in strupper:
        Get_TPS_Current = float(caget('TPS:BeamCurrent'))
        TPS_Current_Result = TextSendMessage(
            text="TPS Current:\n%.4f mA" % Get_TPS_Current)
        return TPS_Current_Result

    # Reply All FE Status
    if "INTERLOCK" in strupper and "ALL" in strupper:
        FE02_S = caget('VacFE-Status:02', use_monitor=False)
        FE05_S = caget('VacFE-Status:05', use_monitor=False)
        FE09_S = caget('VacFE-Status:09', use_monitor=False)
        FE21_S = caget('VacFE-Status:21', use_monitor=False)
        FE23_S = caget('VacFE-Status:23', use_monitor=False)
        FE24_S = caget('VacFE-Status:24', use_monitor=False)
        FE25_S = caget('VacFE-Status:25', use_monitor=False)
        FE41_S = caget('VacFE-Status:41', use_monitor=False)
        FE44_S = caget('VacFE-Status:44', use_monitor=False)
        FE45_S = caget('VacFE-Status:45', use_monitor=False)
        text = "FE各段狀態如下 :\n" +\
            "● FE-02 Status: %s \n" % FE02_S +\
            "● FE-05 Status: %s \n" % FE05_S +\
            "● FE-09 Status: %s \n" % FE09_S +\
            "● FE-21 Status: %s \n" % FE21_S +\
            "● FE-23 Status: %s \n" % FE23_S +\
            "● FE-24 Status: %s \n" % FE24_S +\
            "● FE-25 Status: %s \n" % FE25_S +\
            "● FE-41 Status: %s \n" % FE41_S +\
            "● FE-44 Status: %s \n" % FE44_S +\
            "● FE-45 Status: %s" % FE45_S
        text = text.replace("Error!**", "❗️")
        text = text.replace("Normal", "✔️")
        Interlock_All_Result = TextSendMessage(text=text)
        return Interlock_All_Result

    # interlock+STATUS+number
    if "VALVE" in strupper and "STATUS" in strupper and "FE" in strupper:  # unfinished
        str = event.message.text
        FE_number = re.sub("\D", "", str)  # take out FE number
        print('Interlock Index:%s' % FE_number)
        if bool(FE_number) == True:
            # try:
            Valve_Status_Text = Valve_Status(FE_number)
            if Valve_Status_Text == 0:
                return 0
            else:
                Valve_Status_Result = TextSendMessage(text=Valve_Status_Text)
                return Valve_Status_Result
        else:
            print("No Index:No FE number in text")
        return 0

    # interlock+FALSE+number
    if "INTERLOCK" in strupper and "ALARM" in strupper:  # unfinished
        try:
            str = event.message.text
            FE_number = re.sub("\D", "", str)  # take out FE number
            print('Interlock Index:%s' % FE_number)
            if bool(FE_number) == True:
                error_text = FE_Diagnosis(FE_number)
                if error_text == 0:
                    return 0
                else:
                    Error_Result = TextSendMessage(text=error_text)
                    return Error_Result
            else:
                print("No Index:No FE number in text")
        except:
            print("Error")
        return 0

    if "XBPM" in strupper and "FE" in strupper:  # unfinished
        str = event.message.text
        FE_number = re.sub("\D", "", str)  # take out FE number
        print('XBPM index:%s' % FE_number)
        if bool(FE_number) == True:
            try:
                # Use EPICS to get XBPM value
                XBPM_1X, XBPM_1Y, XBPM_2X, XBPM_2Y = XBPM_Status(FE_number)
                # Use LINE message API reply method return the result
                XBPM_Reuslt = TextSendMessage(text="FE%s XBPM Position:\n" % FE_number +
                                              "● 1X: %s um\n" % XBPM_1X +
                                              "● 1Y: %s um\n" % XBPM_1Y +
                                              "● 2X: %s um\n" % XBPM_2X +
                                              "● 2Y: %s um" % XBPM_2Y)
                return XBPM_Reuslt
            except:
                print("No Index")
                return 0
        else:
            print("No Index")
        return 0
# -----------------------------------------------------------------------------20181227
    if "VACUUM" in strupper and "STATUS" in strupper:
        str = event.message.text
        FE_number = re.sub("\D", "", str)
        print('Vacuum index:%s' % FE_number)
        if bool(FE_number) == True:
            Vacuum_msg = FE_VacPresure(FE_number)
            print(Vacuum_msg)
            if Vacuum_msg == 0:
                return 0
            else:
                Vacuum_Result = TextSendMessage(text=Vacuum_msg)
                return Vacuum_Result
        else:
            print("No Index")
            return 0

    if "TEMP" in strupper and "STATUS" in strupper:
        str = event.message.text
        FE_number = re.sub("\D", "", str)
        print('Temp index:%s' % FE_number)
        if bool(FE_number) == True:
            Temp_msg = FE_Temp(FE_number)
            print(Temp_msg)
            if Temp_msg == 0:
                return 0
            else:
                TEMP_Result = TextSendMessage(text=Temp_msg)
                return TEMP_Result
        else:
            print("No Index")
            return 0

    if "ID" in strupper and "GAP" in strupper and "FE" in strupper:
        str = event.message.text
        FE_number = re.sub("\D", "", str)
        print('ID index:%s' % FE_number)
        if bool(FE_number) == True:
            ID_Gap_msg = ID_Gap_Result(FE_number)
            ID_Gap = TextSendMessage(text=ID_Gap_msg)
            return ID_Gap
        else:
            print("No Index")
            return 0

    if "CAROUSEL" in strupper and "TEMP" in strupper:
        TEMP_carousel = TemplateSendMessage(
            alt_text='Carousel template', template=FE_Temp_Carousel())
        return TEMP_carousel

    if "CAROUSEL" in strupper and "INTERLOCK" in strupper:
        INTERLOCK_carousel = TemplateSendMessage(
            alt_text='Carousel template', template=Interlock_Carousel())
        return INTERLOCK_carousel

    if "CAROUSEL" in strupper and "VACUUM" in strupper:
        VACUUM_carousel = TemplateSendMessage(
            alt_text='Carousel template', template=FE_Vacuum_Carousel())
        return VACUUM_carousel

    if "CAROUSEL" in strupper and "VALVE" in strupper:
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template', template=FE_Valve_Carousel())
        return carousel_template_message

    if "CAROUSEL" in strupper and "XBPM" in strupper:
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template', template=XBPM_Carousel())
        return carousel_template_message

    if "CAROUSEL" in strupper and "ID" in strupper:
        carousel_template_message = TemplateSendMessage(
            alt_text='ID Gap Status', template=ID_Gap_Carousel())
        return carousel_template_message
    return 0
