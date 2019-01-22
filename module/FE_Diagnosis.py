from epics import caget
from multiprocessing import Process, Queue
import re
import os
# =====================================================
Front_End = ["02", "05", "09", "21", "23", "25", "41", "44", "45"]
# =====================================================


def MP_FE_Diagnosis(line_reply_token, Message, line_bot_api, TextSendMessage):
    print("parent process:", os.getppid())
    print("process id:", os.getpid())
    try:
        str = Message
        FE_number = re.sub("\D", "", str)  # take out FE number
        print('Interlock Index:%s' % FE_number)
        if bool(FE_number) == True:
            error = FE_Diagnosis(FE_number)
            if error == 0:
                return 0
            else:
                line_bot_api.reply_message(
                    line_reply_token, TextSendMessage(text=error))
        else:
            print("No Index:No FE number in text")
    except:
        print("MP_Error")
    print("MP_FE_Diagnosis END")
    return 0


def FE_Diagnosis(FE_Item):
    if FE_Item in Front_End:
        try:
            error = "⚠️FE%s Interlock Warning: \n" % FE_Item
            if FE_Item in Front_End:
                Status = caget('VacFE-Status:%s' % FE_Item)
                if Status == "Error!**":
                    print(Status)
                    IG1_Setpoint = caget("FE-%s-IG1:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    IG2_Setpoint = caget("FE-%s-IG1:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)

                    IP1_Setpoint = caget("FE-%s-IP1:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    IP2_Setpoint = caget("FE-%s-IP2:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    IPA_Setpoint = caget("FE-%s-IPA:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    IPB_Setpoint = caget("FE-%s-IPB:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    IPC_Setpoint = caget("FE-%s-IPC:SetPoint1" %
                                         FE_Item, use_monitor=False, timeout=0.1)

                    FS1_Setpoint = caget("FE-%s-FS1:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    FS2_Setpoint = caget("FE-%s-FS2:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    FS3_Setpoint = caget("FE-%s-FS3:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    FS4_Setpoint = caget("FE-%s-FS4:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    FS5_Setpoint = caget("FE-%s-FS5:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    FS6_Setpoint = caget("FE-%s-FS6:SetPoint" %
                                         FE_Item, use_monitor=False, timeout=0.1)
                    CP_Air = caget("FE-%s-CP-Air:SetPoint" %
                                   FE_Item, use_monitor=False, timeout=0.1)
                    BL_Vaccum = caget("FE-%s-BLA:Vacuum" %
                                      FE_Item, use_monitor=False, timeout=0.1)

                    if not IG1_Setpoint:
                        error = error+"IG1 False \n"
                    if not IG2_Setpoint:
                        error = error+"IG2 False \n"

                    if not IP1_Setpoint:
                        error = error+"IP1 False \n"
                    if not IP2_Setpoint:
                        error = error+"IP2 False \n"
                    if not IPA_Setpoint == True:
                        error = error+"IPA False \n"
                    if not IPB_Setpoint == True:
                        error = error+"IPB False \n"
                    if not IPC_Setpoint == True:
                        error = error+"IPC False \n"

                    if not FS1_Setpoint == True:
                        error = error+"FS1 False \n"
                    if not FS2_Setpoint == True:
                        error = error+"FS2 False \n"
                    if not FS3_Setpoint == True:
                        error = error+"FS3 False \n"
                    if not FS4_Setpoint == True:
                        error = error+"FS4 False \n"
                    if not FS5_Setpoint == True:
                        error = error+"FS5 False \n"
                    if not FS6_Setpoint == True:
                        error = error+"FS6 False \n"

                    if not CP_Air == True:
                        error = error+"CP Air False \n"
                    if not BL_Vaccum == True:
                        error = error+"BL Vacuum False \n"
                    error = error.rstrip(" \n")
                    print(error)
                else:
                    error = "✅ FE%s Interlock: Normal" % FE_Item
            else:
                return 0
        except:
            print("CA ERROR!")
            return 0
        finally:
            return error
    else:
        print("No Index(in module)")
        return 0


def Valve_Status(FE_Item):
    if FE_Item in Front_End:
        try:
            Valve_Status = "FE%s Valve Status:\n" % FE_Item
            if caget('FE-%s-PAB:Open' % FE_Item, timeout=0.1) == True:
                Valve_Status = "✳️ "+Valve_Status+"● PAB Open\n"
            if caget('FE-%s-PAB:Close' % FE_Item, timeout=0.1) == True:
                Valve_Status = "\uD83D\uDD34 "+Valve_Status+"● PAB Close\n"
            if caget('FE-%s-MGV:Open' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● MGV Open\n"
            if caget('FE-%s-MGV:Close' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● MGV Close\n"
            if caget('FE-%s-FCV:Open' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● FCV Open\n"
            if caget('FE-%s-FCV:Close' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● FCV Close\n"
            if caget('FE-%s-HMS:Open1' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● HMS Open\n"
            if caget('FE-%s-HMS:Close1' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● HMS Close\n"
            if caget('FE-%s-GV1:Open' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● GV1 Open"
            if caget('FE-%s-GV1:Close' % FE_Item, timeout=0.1) == True:
                Valve_Status = Valve_Status+"● GV1 Close"

            return(Valve_Status)
        except:
            return 0
    else:
        print("No Index(in module)")
        return 0


def FE_VacPresure(FE_Item):
    if FE_Item in Front_End:
        Vacuum_Status = "FE%s Vacuum Status:\n" % FE_Item
        IG1 = caget('FE-%s-IG1:Pressure' % FE_Item)
        #IG1_fix = (10**(IG1-10))*(10**9)
        IG1_msg = "● IG1: %.2f nPa \n" % (IG1)

        IG2 = caget('FE-%s-IG2:Pressure' % FE_Item)
        #IG2_fix = 10**((IG2-7.2)/0.6)*130*(10**9)
        IG2_msg = "● IG2: %.2f nPa \n" % (IG2)

        IP1 = caget('FE-%s-IP1:Pressure' % FE_Item)
        #IP1_Fix = 10**(IP1*1.2-9)*(10**9)
        IP1_msg = "● IP1: %.2f nPa \n" % (IP1)

        IP2 = caget('FE-%s-IP2:Pressure' % FE_Item)
        #IP2_Fix = 10**(IP2*1.2-9)*(10**9)
        IP2_msg = "● IP2: %.2f nPa \n" % (IP2)

        IPA = caget('FE-%s-IPA:Pressure' % FE_Item)
        #IPA_Fix = 10**(IPA*1.2-9)*(10**9)
        IPA_msg = "● IPA: %.2f nPa \n" % (IPA)

        IPC = caget('FE-%s-IPC:Pressure' % FE_Item)
        #IPC_Fix = 10**(IPC*1.2-9)*(10**9)
        IPC_msg = "● IPC: %.2f nPa" % (IPC)
        print(123)
        Vacuum_Status = Vacuum_Status+IG1_msg+IG2_msg+IP1_msg+IP2_msg+IPA_msg+IPC_msg
        return(Vacuum_Status)
        # except: return 0
    else:
        print("No Index(in module)")
        return 0


def FE_Temp(FE_Item):
    if FE_Item in Front_End:
        Temp_Status = "FE%s Temp Status:\n" % FE_Item
        T1_in = caget('FE-%s-DIW-in:T1' % FE_Item)
        T1_in_msg = "● T1 In: %.2f °C \n" % (T1_in)
        T1_out = caget('FE-%s-DIW-out:T1' % FE_Item)
        T1_out_msg = "● T1 Out: %.2f °C \n" % (T1_out)
        T2_out = caget('FE-%s-DIW-out:T2' % FE_Item)
        T2_out_msg = "● T2 Out: %.2f °C \n" % (T2_out)
        T3_out = caget('FE-%s-DIW-out:T3' % FE_Item)
        T3_out_msg = "● T3 Out: %.2f °C" % (T3_out)
        Temp_Status = Temp_Status+T1_in_msg+T1_out_msg+T2_out_msg+T3_out_msg
        return(Temp_Status)
    # except: return 0
    else:
        print("No Index(in module)")
        return 0
