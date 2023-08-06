# Holm10 Nov 5 2019, based on rdcontdt.py

def rundt(  dtreal,nfe_tot=0,savefn='../solutions/savedt',dt_tot=0,ii1max=500,ii2max=5,ftol_dt=1e-5,itermx=7,rlx=0.9,n_stor=0,
            tstor_s=1e-3,tstor_e=4e-2,incpset=7,dtmfnk3=1e-4):
    ''' Function advancing case time-dependently: increasing time-stepping is the default to attain SS solution
    rdrundt(dtreal,**keys)

    Variables
    dtreal                  The inital time step time

    Keyword parameters:
    nfe_tot[0]              Number of function evaluations
    savefn[savedt]          Name of hdf5 savefile written every time-step
    dt_tot[0]               Total time accummulated: default option resets time between runs    
    ii1max[500]             Outer loop (dt-changing) iterations
    ii2max[5]               Inner loop (steps at dt) iterations
    ftol_dt[1e-5]           Time-dependent fnrm tolerance 
    itermx[7]               Max. number of linear iterations allowed
    rlx[0.9]                Max. allowed change in variable at each iteration
    n_stor[0]               Number of linearly spaced hdf5 dumps 
    tstor_s[1e-3]           Start time for storing hdf5 files
    tstor_e[4e-2]           End time for storing hdf5 files
    incpset[7]              Iterations until Jacobian is recomputed
    dtmfnk[1e-4]            dtreal for mfnksol signchange if ismfnkauto=1 (default)
    The above defaults are based on rdinitdt.

    Additional UEDGE parameters used in the function, assuming their default values are:
    bbb.rdtphidtr[1e20]     # Ratio dtphi/dtreal
    bbb.ismfnkauto[1]       # If =1, mfnksol=3 for dtreal<dtmfnk3, otherwise=-3
    bbb.mult_dt[3.4]        # Factor expanding dtreal after each successful inner loop
    bbb.itermxrdc[7]        # Itermx used by the script
    bbb.ftol_min[1e-9]      # Value of fnrm where time advance will stop
    bbb.t_stop[100]         # Value of dt_tot (sec) where calculation will stop
    bbb.dt_max[100]         # Max. time step for dtreal
    bbb.dt_kill[1e-14]      # Min. allowed time step; rdcontdt stops if reached
    bbb.deldt_min[0.04]     # Minimum relative change allowed for model_dt > 0
    bbb.initjac[0]          # If=1, calc initial Jac upon reading rdcontdt
    bbb.numrevjmax[2]       # Number of dt reductions before Jac recalculated
    bbb.numfwdjmax[1]       # Number of dt increases before Jac recalculated
    bbb.ismmaxuc[1]         # =1 for intern calc mmaxu; =0,set mmaxu & dont chng
    bbb.irev[-1]            # Flag to allow reduced dt advance after cutback
    bbb.ipt[1]              # Index of variable; value printed at step
                            # If ipt not reset from unity, ipt=idxte(nx,iysptrx+1)
   

    Additional comments (from rdcontdt):
    This file runs a time-dependent case using dtreal.  First, a converged solution for a (usually small) dtreal is obtained:
    UEDGE must report iterm=1 at the end. Then the control parameters are adjusted. If a mistake is made, to restart this file 
    without a Jacobian evaluation, be sure to reset iterm=1 (=> last step was successful)


    '''
    from uedge import bbb,com
    from uedge.hdf5 import hdf5_save
    from numpy import sqrt

 

    # Store the original values
    dt_tot_o=bbb.dt_tot
    ii1max_o=bbb.ii1max
    ii2max_o=bbb.ii2max
    ftol_dt_o=bbb.ftol_dt 
    itermx_o=bbb.itermx   
    rlx_o=bbb.rlx    
    n_stor_o=bbb.n_stor   
    tstor_s_o=bbb.tstor_s  
    tstor_e_o=bbb.tstor_e 
    incpset_o=bbb.incpset 
    dtmfnk3_o=bbb.dtmfnk3
    icntnunk_o=bbb.icntnunk
    ftol_o=bbb.ftol



    # Set inital time-step to dtreal
    bbb.dtreal=dtreal

    # Check if successful time-step exists (bbb.iterm=1)
    if (bbb.iterm == 1):
        print("Initial successful time-step exists")
        bbb.dtreal = bbb.dtreal*bbb.mult_dt #compensates dtreal divided by mult_dt below
    else:
        print("*---------------------------------------------------------*")
        print("Need to take initial step with Jacobian; trying to do here")
        print("*---------------------------------------------------------*")
        bbb.icntnunk = 0
        bbb.exmain()
        bbb.dtreal = bbb.dtreal*bbb.mult_dt #compensates dtreal divided by mult_dt below

    if (bbb.iterm != 1):
        print("*--------------------------------------------------------------*")
        print("Error: converge an initial time-step first; then retry rdcontdt")
        print("*--------------------------------------------------------------*")
        return
    
    # Set UEDGE variables to the prescribed values
    bbb.dt_tot=dt_tot
    bbb.ii1max=ii1max
    bbb.ii2max=ii2max
    bbb.ftol_dt=ftol_dt 
    bbb.itermx=itermx   
    bbb.rlx=rlx    
    bbb.n_stor=n_stor   
    bbb.tstor_s=tstor_s  
    bbb.tstor_e=tstor_e 
    bbb.incpset=incpset 
    bbb.dtmfnk3=dtmfnk3



    # Saved intermediates counter
    i_stor=0
    dt_stor = (bbb.tstor_e - bbb.tstor_s)/(bbb.n_stor - 1)



    nfe_tot = max(nfe_tot,0)
    deldt_0 = bbb.deldt
    isdtsf_sav = bbb.isdtsfscal

    if (bbb.ipt==1 and bbb.isteon==1): 	# set ipt to te(nx,iysptrx+1) if no user value
        ipt = bbb.idxte[com.nx-1,com.iysptrx]  #note: ipt is local, bbb.ipt global

    bbb.irev = -1         # forces second branch of irev in ii1 loop below
    if (bbb.iterm == 1):  # successful initial run with dtreal
        bbb.dtreal = bbb.dtreal/bbb.mult_dt     # gives same dtreal after irev loop
    else:                 # unsuccessful initial run; reduce dtreal
        bbb.dtreal = bbb.dtreal/(3*bbb.mult_dt) # causes dt=dt/mult_dt after irev loop
       
    if (bbb.initjac == 0): bbb.newgeo=0
    dtreal_sav = bbb.dtreal
    bbb.itermx = bbb.itermxrdc
    bbb.dtreal = bbb.dtreal/bbb.mult_dt	#adjust for mult. to follow; mult_dt in rdinitdt
    bbb.dtphi = bbb.rdtphidtr*bbb.dtreal
    neq=bbb.neq
    svrpkg=bbb.svrpkg.tostring().strip()
    #
    bbb.ylodt = bbb.yl
    bbb.pandf1 (-1, -1, 0, bbb.neq, 1., bbb.yl, bbb.yldot)
    fnrm_old = sqrt(sum((bbb.yldot[0:neq]*bbb.sfscal[0:neq])**2))
    if (bbb.initjac == 1): fnrm_old=1.e20
    print("initial fnrm =",fnrm_old)

    for ii1 in range( 1, bbb.ii1max+1):
        if (bbb.ismfnkauto==1): bbb.mfnksol = 3
        # adjust the time-step
        if (bbb.irev == 0):
            # Only used after a dt reduc. success. completes loop ii2 for fixed dt
            bbb.dtreal = min(3*bbb.dtreal,bbb.t_stop)	#first move forward after reduction
            bbb.dtphi = bbb.rdtphidtr*bbb.dtreal
            if (bbb.ismfnkauto==1 and bbb.dtreal > bbb.dtmfnk3): bbb.mfnksol = -3
            bbb.deldt =  3*bbb.deldt
        else:
            # either increase or decrease dtreal; depends on mult_dt
            bbb.dtreal = min(bbb.mult_dt*bbb.dtreal,bbb.t_stop)
            bbb.dtphi = bbb.rdtphidtr*bbb.dtreal
            if (bbb.ismfnkauto==1 and bbb.dtreal > bbb.dtmfnk3): bbb.mfnksol = -3
            bbb.deldt =  bbb.mult_dt*bbb.deldt
          
        bbb.dtreal = min(bbb.dtreal,bbb.dt_max)
        bbb.dtphi = bbb.rdtphidtr*bbb.dtreal
        if (bbb.ismfnkauto==1 and bbb.dtreal > bbb.dtmfnk3): bbb.mfnksol = -3
        bbb.deldt = min(bbb.deldt,deldt_0)
        bbb.deldt = max(bbb.deldt,bbb.deldt_min)
        nsteps_nk=1
        print('--------------------------------------------------------------------')
        print('--------------------------------------------------------------------')
        print(' ')
        print('*** Number time-step changes = ',ii1,' New time-step = ', bbb.dtreal)
        print('--------------------------------------------------------------------')

        bbb.itermx = bbb.itermxrdc
        if (ii1>1  or  bbb.initjac==1):	# first time calc Jac if initjac=1
            if (bbb.irev == 1):      # decrease in bbb.dtreal
                if (bbb.numrev < bbb.numrevjmax and \
                    bbb.numrfcum < bbb.numrevjmax+bbb.numfwdjmax): #dont recom bbb.jac
                    bbb.icntnunk = 1	
                    bbb.numrfcum = bbb.numrfcum + 1
                else:                          # force bbb.jac calc, reset numrev
                    bbb.icntnunk = 0
                    bbb.numrev = -1		      # yields api.zero in next statement
                    bbb.numrfcum = 0
                bbb.numrev = bbb.numrev + 1
                bbb.numfwd = 0
            else:  # increase in bbb.dtreal
                if (bbb.numfwd < bbb.numfwdjmax and \
                    bbb.numrfcum < bbb.numrevjmax+bbb.numfwdjmax): 	#dont recomp bbb.jac
                    bbb.icntnunk = 1
                    bbb.numrfcum = bbb.numrfcum + 1
                else:
                    bbb.icntnunk = 0			#recompute jacobian for increase dt
                    bbb.numfwd = -1
                    bbb.numrfcum = 0
                bbb.numfwd = bbb.numfwd + 1
                bbb.numrev = 0			#bbb.restart counter for dt reversals
            bbb.isdtsfscal = isdtsf_sav
            bbb.ftol = max(min(bbb.ftol_dt, 0.01*fnrm_old),bbb.ftol_min)
            bbb.exmain() # take a single step at the present bbb.dtreal
            if (bbb.iterm == 1):
                bbb.dt_tot = bbb.dt_tot + bbb.dtreal
                nfe_tot = nfe_tot + bbb.nfe[0,0]
                bbb.ylodt = bbb.yl
                bbb.pandf1 (-1, -1, 0, bbb.neq, 1., bbb.yl, bbb.yldot)
                fnrm_old = sqrt(sum((bbb.yldot[0:neq-1]*bbb.sfscal[0:neq-1])**2))
                if (bbb.dt_tot>=0.9999999*bbb.t_stop  or  fnrm_old<bbb.ftol_min):
                    print(' ')
                    print('*****************************************************')
                    print('**  SUCCESS: frnm < bbb.ftol; or dt_tot >= t_stop  **')
                    print('*****************************************************')
                    break

        bbb.icntnunk = 1
        bbb.isdtsfscal = 0
        for ii2 in range( 1, bbb.ii2max+1): #take ii2max steps at the present time-step
            if (bbb.iterm == 1):
                bbb.itermx = bbb.itermxrdc
                bbb.ftol = max(min(bbb.ftol_dt, 0.01*fnrm_old),bbb.ftol_min)
                bbb.exmain()
                if (bbb.iterm == 1):
                    bbb.ylodt = bbb.yl
                    bbb.pandf1 (-1, -1, 0, bbb.neq, 1., bbb.yl, bbb.yldot)
                    fnrm_old = sqrt(sum((bbb.yldot[0:neq-1]*bbb.sfscal[0:neq-1])**2))
                    print("Total time = ",bbb.dt_tot,"; Timestep = ",bbb.dtreal)
                    print("variable index ipt = ",ipt, " bbb.yl[ipt] = ",bbb.yl[ipt])
                    dtreal_sav = bbb.dtreal
                    bbb.dt_tot = bbb.dt_tot + bbb.dtreal
                    nfe_tot = nfe_tot + bbb.nfe[0,0]
                    hdf5_save(savefn+'_last_ii2.hdf5')
                    if (bbb.dt_tot>=0.999999999999*bbb.t_stop  or  fnrm_old<bbb.ftol_min):
                        print(' ')
                        print('*****************************************************')
                        print('**  SUCCESS: frnm < bbb.ftol; or dt_tot >= t_stop  **')
                        print('*****************************************************')
                        break
                    print(" ")
    ##       Store variables if a storage time has been crossed
                    if (bbb.dt_tot >= dt_stor*(1+i_stor) and i_stor<bbb.n_stor):
                        hdf5_save(savefn+'dt_tot='+str(bbb.dt_tot)+'.hdf5')  
                        i_stor = i_stor + 1
       ##          End of storage section
          
        if (bbb.dt_tot>=bbb.t_stop  or  fnrm_old<bbb.ftol_min): break   # need for both loops
        bbb.irev = bbb.irev-1
        if (bbb.iterm != 1):	#print bad eqn, cut dtreal by 3, set irev flag
                    ####### a copy of idtroub script ########################
            # integer ii
            # real8 ydmax 
            scalfac = bbb.sfscal
            if (svrpkg != "nksol"): scalfac = 1/(bbb.yl + 1.e-30)  # for time-dep calc.
            ydmax = 0.999999999*max(abs(bbb.yldot*scalfac))
            itrouble = 0
            for ii in range(neq):
                if (abs(bbb.yldot[ii]*scalfac[ii]) > ydmax):
                    itrouble=ii
                    print("** Fortran index of trouble making equation is:")
                    print(itrouble+1)
                    break
            print("** Number of variables is:")
            print("numvar = ", bbb.numvar)
            print(" ")
            iv_t = (itrouble).__mod__(bbb.numvar) + 1
            print("** Troublemaker equation is:")
            print("iv_t = ",iv_t)
            print(" ")
            print("** Troublemaker cell (ix,iy) is:")
            print(bbb.igyl[itrouble,])
            print(" ")
            print("** Timestep for troublemaker equation:")
            print(bbb.dtuse[itrouble])
            print(" ")
            print("** yl for troublemaker equation:")
            print(bbb.yl[itrouble])
            print(" ")
            ######## end of idtroub script ##############################

            if (bbb.dtreal < bbb.dt_kill):
                print(' ')
                print('*************************************')
                print('**  FAILURE: time-step < dt_kill   **')
                print('*************************************')
                break
            bbb.irev = 1
            print('*** Converg. fails for bbb.dtreal; reduce time-step by 3, try again')
            print('----------------------------------------------------------------- ')
            bbb.dtreal = bbb.dtreal/(3*bbb.mult_dt)
            bbb.dtphi = bbb.rdtphidtr*bbb.dtreal
            if (bbb.ismfnkauto==1 and bbb.dtreal > bbb.dtmfnk3): bbb.mfnksol = -3
            bbb.deldt =  bbb.deldt/(3*bbb.mult_dt) 
            bbb.iterm = 1

    # Restore the original values
    bbb.dt_tot=dt_tot_o
    bbb.ii1max=ii1max_o
    bbb.ii2max=ii2max_o
    bbb.ftol_dt=ftol_dt_o 
    bbb.itermx=itermx_o   
    bbb.rlx=rlx_o    
    bbb.n_stor=n_stor_o   
    bbb.tstor_s=tstor_s_o  
    bbb.tstor_e=tstor_e_o 
    bbb.incpset=incpset_o 
    bbb.dtmfnk3=dtmfnk3_o
    bbb.icntnunk=icntnunk_o
    bbb.ftol=ftol_o
    bbb.dtreal=1e20


