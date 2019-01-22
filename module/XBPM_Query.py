from epics import caget

def XBPM_Status(FE_number):
    try:
        if FE_number =="05":
            XBPM_1X=caget('FE-DI-XBPM-051:signals:sa.X')/1000
            XBPM_1Y=caget('FE-DI-XBPM-051:signals:sa.Y')/1000
            XBPM_2X=caget('FE-DI-XBPM-052:signals:sa.X')/1000
            XBPM_2Y=caget('FE-DI-XBPM-052:signals:sa.Y')/1000
        if FE_number =="09":
            XBPM_1X=caget('FE-DI-XBPM-091:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-091:SA:SA_Y_MONITOR')/1000
            XBPM_2X=caget('FE-DI-XBPM-092:SA:SA_X_MONITOR')/1000
            XBPM_2Y=caget('FE-DI-XBPM-092:SA:SA_Y_MONITOR')/1000
        if FE_number =="21":
            XBPM_1X=caget('FE-DI-XBPM-211:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-211:SA:SA_Y_MONITOR')/1000
            XBPM_2X=caget('FE-DI-XBPM-212:SA:SA_X_MONITOR')/1000
            XBPM_2Y=caget('FE-DI-XBPM-212:SA:SA_Y_MONITOR')/1000
        if FE_number =="23":
            XBPM_1X=caget('FE-DI-XBPM-231:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-231:SA:SA_Y_MONITOR')/1000
            XBPM_2X=caget('FE-DI-XBPM-232:SA:SA_X_MONITOR')/1000
            XBPM_2Y=caget('FE-DI-XBPM-232:SA:SA_Y_MONITOR')/1000
        if FE_number =="25":
            XBPM_1X=caget('FE-DI-XBPM-251:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-251:SA:SA_Y_MONITOR')/1000
            XBPM_2X='None'
            XBPM_2Y='None'
            #XBPM_2X=caget('FE-DI-XBPM-252:SA:SA_X_MONITOR')/1000
            #XBPM_2Y=caget('FE-DI-XBPM-252:SA:SA_Y_MONITOR')/1000
        if FE_number =="41":
            XBPM_1X=caget('FE-DI-XBPM-411:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-411:SA:SA_Y_MONITOR')/1000
            XBPM_2X=caget('FE-DI-XBPM-412:SA:SA_X_MONITOR')/1000
            XBPM_2Y=caget('FE-DI-XBPM-412:SA:SA_Y_MONITOR')/1000
        if FE_number =="45":
            XBPM_1X=caget('FE-DI-XBPM-451:SA:SA_X_MONITOR')/1000
            XBPM_1Y=caget('FE-DI-XBPM-451:SA:SA_Y_MONITOR')/1000
            XBPM_2X=caget('FE-DI-XBPM-452:SA:SA_X_MONITOR')/1000
            XBPM_2Y=caget('FE-DI-XBPM-452:SA:SA_Y_MONITOR')/1000
    except:
        print("CA ERROR!")
        return 0
    finally:
        print('XBPM_Status Function:%s'%FE_number)
        print('1X:%s'%XBPM_1X)
        print('1Y:%s'%XBPM_1Y)
        print('2X:%s'%XBPM_2X)
        print('2Y:%s'%XBPM_2Y)
        return XBPM_1X,XBPM_1Y,XBPM_2X,XBPM_2Y
