   
    
subroutine cal_threat_score(rainobs, rainfcst, num_stn, rs1, rs2, HS, MS, FS, ts   )
     
     real,dimension(num_stn):: rainobs, rainfcst
     real rs1, rs2, ts
     real HS, MS, FS
     

     HS=0
     MS=0
     FS=0
     
     do k= 1, num_stn
        if (rainobs(k) >= rs1 .and. rainobs(k)<=rs2 )then
!             if(rainfcst(k) >= rs1 .and.  rainfcst(k) <= rs2)then
             if(rainfcst(k) >= rs1   )then
                HS=HS+1                             ! 正确 ！ 
             endif
             if(rainfcst(k) < rs1)then
                MS=MS+1                             ! 漏报 ！
             endif
        else if (rainobs(k)< rs1 )then
             if(rainfcst(k) >= rs1  )then
                FS=FS+1                             ! 空报 ！
             endif        
        endif    
    
        
     enddo
     
     if ( HS+MS+FS .ne. 0)then
        ts=HS/(HS+MS+FS)
     else
        ts=0
     endif
     
end subroutine
     
 !==========================================================================================    
     
 subroutine cal_threat_score_bak(rainobs, rainfcst, num_stn, rs1, rs2, HS, MS, FS, ts   )
     
     real,dimension(num_stn):: rainobs, rainfcst
     real rs1, rs2, ts
     real HS, MS, FS
     

     HS=0
     MS=0
     FS=0
     
     do k= 1, num_stn
        if (rainfcst(k) >= rs1 .and. rainfcst(k)<=rs2 )then
             if(rainobs(k) >= rs1 )then
                HS=HS+1                             ! 正确 ！ 
             endif
             if(rainobs(k) < rs1)then
                FS=FS+1                             ! 空报 ！
             endif
        endif    

        if ( rainfcst(k)<rs1 .and. rainobs(k) > rs1 ) MS=MS+1   ! 漏报 ！
        
     enddo
     
     
     if ( HS+MS+FS .ne. 0)then
        ts=HS/(HS+MS+FS)
     else
        ts=0
     endif
     
 end subroutine
  
 
 !==========================================================================================    

 
 
 subroutine cal_threat_score_bin(rainobs, rainfcst, num_stn, rs0, HS, MS, FS, ts   )
     
     real,dimension(num_stn):: rainobs, rainfcst
     real rs0, ts
     real HS, MS, FS, DS
     

     HS=0
     MS=0
     FS=0
     DS=0
     
     do k= 1, num_stn
        if (rainobs(k) > rs0 .and.  rainfcst(k) > rs0) HS=HS+1     !  a
        if (rainobs(k) <= rs0 .and.   rainfcst(k) > rs0)  FS=FS+1  !  b      
    
        if (rainobs(k) > rs0 .and.  rainfcst(k) <= rs0) MS=MS+1    !  c 
        if (rainobs(k) <= rs0 .and.   rainfcst(k) <= rs0)  DS=DS+1 !  d

           
     enddo
     
      ts= (HS+DS)/(HS+MS+FS+DS)
     
 end subroutine
 
 
 
 
 
! an event is forecast and the event occurs (a)
! an event is forecast and the event does not occur (b)
! an event is not forecast and the event occurs (c)
! an event is not forecast and the event does not occur (d) 

! The Threat Score (TS) or Critical Success Index (CSI) combines Hit Rate and False Alarm Ratio into one score for low frequency events. It is calculated as follows:
! TS = CSI = a/(a+b+c)


 !==========================================================================================    
     
 subroutine cal_threat_score_v2(rainobs, rainfcst, num_stn, rs1, rs2, HS, MS, FS, ts   )
     
     real,dimension(num_stn):: rainobs, rainfcst
     real rs1, rs2, ts
     real HS, MS, FS, DS
     

     HS=0
     MS=0
     FS=0
     DS=0
     
     do k= 1, num_stn
        if (rainfcst(k) >= rs1 .and. rainfcst(k)<=rs2 )then
             if(rainobs(k) >= rs1 )then
                HS=HS+1                             ! 正确 ！  a 
             endif
             if(rainobs(k) < rs1)then
                FS=FS+1                             ! 空报 ！  b
             endif
        endif    

        if ( rainfcst(k)<rs1 .and. rainobs(k) > rs1 ) MS=MS+1   ! 漏报 ！  c
        if ( rainfcst(k)<rs1 .and. rainobs(k) < rs1 ) DS=DS+1   ! 正确 ！  d     
     enddo
     
     
     if ( HS+MS+FS .ne. 0)then
        !ts=HS/(HS+MS+FS)
!        ts=(HS+DS)/(HS+MS+FS+DS)
     else
        ts=0
     endif
     
 end subroutine

 
!  subroutine QTS(ts,H,F,M,C)
!  implicit none
!  integer                                ::H,F,M,C !命中，空报，漏报，正确否定
!  real                                ::ts
!
!  ts=H/(H+F+M)
!  return
!  end subroutine


 subroutine cal_fcst_verification(rainobs, rainfcst, num_stn, s1, s2, rr)
 real, dimension(num_stn):: rainobs, rainfcst
 
 real s1, s2, s3, rr, sxy, sxx, syy
 
 
 s1=0
 s2=0
 s3=0
 
 do k=1, num_stn
 
    s1=s1+abs( rainobs(k)-rainfcst(k) )/ real(num_stn)  ! 绝对平均误差
    
    s2= s2 + ( rainobs(k)-rainfcst(k) )**2.0            !  均方差
    
    sxy= sxy + rainobs(k)*rainfcst(k)
    sxx= sxx + rainobs(k)*rainobs(k)
    syy= syy + rainfcst(k)*rainfcst(k)  
 enddo
 
    s2 = sqrt( s2/real(num_stn) )
        
    rr = sxy/( sqrt(sxx)*sqrt(syy) )                    ! 相关系数
 
 endsubroutine 