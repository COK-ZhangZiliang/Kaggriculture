"""Kaggriculture V2: public-route economic planner with state-safe repairs.

Third-party route provenance:
- Author: Kaito Fukami.
- Notebook: https://www.kaggle.com/code/kaitofukami/177-180-fresh-top-30-v21-1-conditional-memory
- Source artifact SHA-256:
  d9dc24ce5429ec628ead0621a160bee90725350683d7dfcc4686fcaf511f3aab
- Changes: only the 719-action route was extracted, re-serialized, and
  compressed; the source controller and prototype memory were replaced.

The controller around the route is independently implemented for this
repository. Apache-2.0 applies only to the third-party route portion; the
submission bundle carries the license and detailed third-party notice.
"""

import base64
import copy
import json
import math
import zlib


_ROUTE_B85 = (
    'c-rk<U2hyoa{MoR=7Z*g6y-OrG<On?D+(0l!FfR}7PvDE80Uwz-wgkEYsq1EPiJIgWLEWv+P${{In!O0Rb8DK85#N0|DOH(FTeid'
    '@4ue?%TH&Yu0MZ1dpJM)k6-@lZ~y)E4_`n2<CkCm^Y8!j_47|>??2q_zW!JH@WYqC{(SxM!;jZDXXj_1-|u#x&d%57A8&8>lRtmn'
    '?cRO;<Np2b`u^<v_3Y0-?rv^Bo}I7O4-fx$el+S2Z~yY;)8uNy_<uUv?>^r@j_2d;-TnK=PlriPem5Q7(+`d({@Wlv-QB+X^7eil'
    'o*BjuUq0Nt`}ynD@4r0SU^0sF=4=?lg~#tr$1$Jv&Gp;eVbc1|%s<H;4z`<IdOk&X3-?RpR>XG03VxmN$I<@BCOp{UX(1c!_k5qH'
    '{r0#guJ3nu$9MeGZ+mh&s>8Qa<{Ym(PV)H%Z?6x=JAA2=@y1CFcN)H9w|+PSyC%R^c0<g5##ia+2BP)shKSAhe7&UkhMmx0KDyP0'
    'ouF^E`E^CBjXR->vG9XBpKxTg`8!Fp+T>5V+03mvSqsd;w}|=I<l!n93mC+=k?=s0shAI)Ok_VeM(Z~2nXS5w`}o7@FMBvk90w2j'
    'IUCpA8orRap7EOw2WZnZ=11$d8b`st<{Hl~)$d|5yX*Fa=`oJCw>LMtxA#B)X?J)3;pW4?9lyLPSNweYrG1(D59{6C?Wbj*rq8>Z'
    '-$J*^kjDsakqr@^K&!^<y_hGC8NR%8GW)jIO+ZYW+)XORP*`1#3dE7)e5I$C8J%_gdh_$`=z3@cjE4nHIzAkZrB)ANfHDpQ_`lYt'
    'Yq+;H>ga@7qjsHkll@~OBo4<ML=YPxb88aNmDax3v_aVN2c0)KNfw&88xeK7_uL79(;YrMeS5iE{{d#rU*t+GyqFEht$&{;D1`Pe'
    '_0D~-|2<u8=HG5J{_R%vZ@Htp#o08)vr>{`hl?qwBXgj@E#|iuBBhk8n!IJ3xsI|(HE(~8lJ>S03V@hfIs0Gbmez=NMj$5%58A2|'
    'PwrTlV&+Z8UhDN65}Sq)d=J=7ykARHxas)PPQ1tx12X8zHyFc<GYUv-{^4x`4&8qmrB_z#MGoP+P7E$}*|uEa<GL>AL0@>pvpyd5'
    'G(hX^LsK5tLQeF+bZK&;3Dv1#D!{9bA;jgZXD2z*gcJuU0gf~3SOZEfxPwyMB20I)7(hP!@BQ`Nzp9S#MnFmr&Oe{JPO2G(2k(L6'
    '+4<(K@(%6r$FV4sHfx&c?{UD48H405$d@vg8O$X`c>);Dj5J^WOulve)ASR#bTnuJWg{9P&SVM9EJDG2zTb4w?M&d)mstVADD)C^'
    '^0Q~Hc=QBVLyl_}+b;CL&BVZtI8Zu<|K+yCFadDo`JBR28fNR0bEdoBS<ZOoX+-w<6?5UtYvY$QV4T$;r{+N^I7|f~G4(2Vx=3nZ'
    'Xo*t845J1&c212mO@<VH;(>mtf!VZHIIyJ6D+YAyA;RIhm{`NXn4GYOK(!pr)sXp*@{?sk`-`TC{<3fAzUd#apDa%Amg2Inh(&|)'
    'J_ceFs@R8(8yTo08I2$(of$#7K(Q-3BS*usD|otT$E&?bWKQg~8Hl8xA)8zhSa}#TsE9(GON1_d6jmId!Zm7QZ)N=#J5~a_$8*o6'
    'DV6xVA(xc2MT#P}UvS)tSyF>d8e;B^T!<m<)V12*-rhXc%y;m%ZmvJR%h&eDaoW6mAG<fmI}p9XH?us?=li?s{SUjlyT6{DU&SwA'
    'TJ`QHdzQ=6%t=S%aqBA@By0b@s1;vtJP9-RP%J%O8T{{gAVb1q_MN4z?G>5(I9B+UVRj!bK2OA<q{C#7x2^%GZb7f+zARbbuK-Jc'
    '9LZpbg=yo+&_@Gdn|VHiPNNh97f&tY_+$$<QVSK^Y`S3`hY$07X^?bj@WJJ!1qDgy2o$jNEg|(Lmeg7e9mLs%Obm`eAfvC1tqH~~'
    'tm_3Ka};wg?kcwy<0Qrk{B`n9h1t&dAn9m3wC_WECfHPop(^A<7O8a|Oh3k*II@mR%=2!bd9S-QaVY!J(^_Juqu_*VoJ}K>Z6b7<'
    '9^LR|E^3T5K<}$p@!Mfk&9W8zc;LxTg2#XLASOkfI}LLHzGvIW-aP2R0J_sKZ2GMV^)0isMj37XKG@Bj7BIFhgCq+J0vWrmb~J&j'
    'B94pd2e7yiiGg|61-!V07My#UA@e9Qw44-rm3<lWXqKTI?tnY(Q^>0V=sLDH<}Y<IDZr`C^A0F^4x`G^Hw(*&v~wMjD#4l)YNF4#'
    '3~^%BV<hZ4=eePDP@f>)oIIKE-be|b%K*-0gTUD>5&a<l5ZKB7uPvd()%6g!wlV?>Rd{EsSs}>Kl;k@r!-DZ)>N)F`j*$&SnVw4~'
    'wX_?vv4p7dTojC7*WH=$=1<qolH2>;pG3(&ez^I|Z=4{JxSF$4qzpuI&FQ#Q&iqYDx|7-0mAj!p_cTg<osUx2YLvQaic+6G)JR)a'
    '1feB3onJ2X-ka$Q<G?8wixxA0v$~=Ht?xGyk}j}Gjpr<#77ROykMT;ir2?*!9t6<=7wE=z*~mir*%m+EC=jh}EEC%Y6ne=qa0P0l'
    'x8~s?S=5R*1$Km8!Z05xCX4gFjh1!HEU=zaV2RXl7c#ek5lA}{zjCZH@lk9<#R=?auf{$7j#AaCWkSCzH45mwBIdZOQNF|qMaY)4'
    '6rI<rNg1WrAczZpvN0@>Bdg~LAL)PFMbd=dznNa3Rhq^1&l`dxmY7iDwGH~?g&w+L5PF@7;VcyrXBa{DVj;37a~X$G(2Qfla1<R5'
    'mO$*wWR)Z&Y`km#!db!Pm9lR8U=h1gG6k|q-Q)CHyH-}X!Ou-BQJw_BZLrtHBwtVFC^8`M7}47LQWy=CL*OgXfzi_{#h=^sQxD?{'
    'Zv#~LeQAFt7>VNIv;7Ico4%Azu=+k35<m1tgQ7P9P_!ekm4!U){#cGR8RotT-(#GNv@6@J$&c-ED8MsdSkioumwKr*<)Hcxg+N-F'
    'ec<DbO*gd|9oP72JeKfK!z7ld;uFD{T;3$H2ghcp=TWc+EC}|JyoPf%nxggWg`><`?$5(8S$^=zh?gd5w#hueVNq#1ZRs_-rB5ii'
    'SCpz;Ffn<U%jT7ngneB~PimEjQQu$y79l<@FY$x_Mdw_VDLhTKuESPX+kkI7wbA$hgY&?T{6b1$okA?gcX+jaKH|z=^laiRQeG$='
    'p4QCxrG+d4l_rGdUzw30rC@2nz?yVnSWuRph`zldqAkdH$7N#y7YWSEuQ}@@>5jP9TA3S?r(}(JgIuj+8_5%I68jhyk`);13}za0'
    'kevExGgCMR8W(r15uI-J*{Kt)TFCvjUJ^Z_YGuV4P{YTs$P+zpS1sqQ#~;eXeWL%_7Z(ALX3QE_X|>db3l)3<@~6s@&^I)tT89U`'
    '5217l;x)O(^J4WYi#Bjnu2XdS+Cdi~W#k@-%nqJ)o$8WNV14aQ|Mf$aJ|8_8LVNm<;6Mq^T6IE$Ddsb9+->z?kmwUS)r#0R2Fo%V'
    '!qzT?yHpSirp%XdP7x|g$m9)k=2@0#Vd{h)^g7%HU{N?_09k2Pz-3UymqLz3G+KK^<MPLhW*^NMGU-Hn3gXtGauHc_8ysLtv9f_w'
    'pHMaK{N9(!ITj!Z0jNK>S33_pr3;t(5ZA&iD}i8(Y5<Hr-HoePU4#<SWhNIz@YXViN}_YCZKY^lLbQ5Qlq~2q4g-~W%Vj!MM8du|'
    'K|<6gMf3q<+2UA&P=S)PuB=Q1N4jDPomVFG9+|{K3z;Ufa&{jDT$L8A>7uMZkn_f3%Qrx&mpY`hS9tMSeG}={qGMjQ4)=t&(n;EI'
    'D|zH&s*Yd|kTfDFktK}A^azGC$P6(j@W7w1$|?q71!}L8X`yAkIj~$5FB|uIv5ei=-fI{ob|4FT&ZXi;Wl#xw>*$?w=ip(fN(c~z'
    '0<s2*X0;_I<jEZ>2AQpWl8r$%3<7dfF1k&bYsL$LV0GLytkS+F9pBNn&Lh|BstyU1B?h+69o}><J&}q_)^W`T@9EM*K_DB&W%(pc'
    'vSyUv+>15A;x(IQY`wp-0w4~dBDs701tHnryauTCGpDj*eOP~O_l5^g*KDs<$rA^x+6$ECugRZWN<y;+6dg#C?2u`bLT*d-w0E*N'
    'fuv8*s6>s^XI0^7YXMvs7-0UbX00o~J|k2VEF1uof59I(KjBg6Jb5k;#X4xlC|%0m8U09W@LQ>SS66?h631I?p-8-7ak%_oblL&2'
    'cs|DLXC#1Nu{PXpW~qmbWPvfVj~az8NZNY3WvbCm&vw2~;m;dW4&!B|u1ZNMA<NTI|7;!C)3?c+9W{)adF+ezVRXyi`xLm-TG?4J'
    '&?iw8XF4)QUDvvQdX?&Z(mss6Pi@+<(45vi@ZDRc3!^evKVdLWQg-6*0+*iz6DGbqK_ePwimo(fTEM_u&v;ifwH&dpVC#9tdm_Pa'
    'W$G0?CDD)qynM*0L?c9#orXONml;QWmb+h$U<pjIR|Pt>o3gT0a?fUsI(Cyp90?XKawWn0C#*i!n;At(70&c0K)u(0b0w^(>|G~d'
    'EW4yErKV52)r+6n=JGpDDA<MXs8(EOj8RWK&v}F6ZB9)foLJTEO+fgq8H^JRvo+BnHE0dUV~giQ)YJe&ko&ASy(@#c8MeoGfxUAp'
    'D(Fj#eov8tA(R!mEIy;Lf10L4ZSM)PIc!$I@0Q}T?kS(FDQUS-$K;SFP!v4nz`%Mx`an>aCQEn*o7L>1kuH&D;g!HrLE!k$fvS^`'
    'zef@|<op58gVa8#sUgWmqS~?1>RA=7<b~vay0G+U%2iX-7KmJh)C<dwVK!f8h+5><yi@euAU8w$Mw-to4;RYKEj@VquFmAZfNa|7'
    '2ONpKHA{!JE0(87i(;|bYTbvk*sC&aEeKRgzuC5GYi}RABoNnO&Dhf7+BB>^dc8dl-L!HB)0=*0vs`}C0t~}x;Wq>7oVz4yFc3JC'
    '$aAP@R7<>(r3NUB9lSzq?68K;@kquqd~+Vq4S!xffl391DdrH@L1mJ8H4;77Ar|Pq%Vz;`01G0z<J~a*nYbY`<7I_Ze(zqoGu#HE'
    'e9XD{hkv3Xb^8YG`%R)W4wM)L?8D=ghktJ^lOz3=YhYLv$RfC3t}8%-i|b%Wps|DZ1nMciOa-0M9D=op*}6)Bvnzu+6i5maqac1R'
    '$5c>Z8&ZCzYiNFz>ldXgORV??Mp<i=OC{LBQ6t978PLHRiAtY`#&Jso8@4aNNOuC^nox)%t8_1*TQ8jN-ge4&ub1n^+pLG;e1eK{'
    '%Ve;f*fCBE_fBS-H*B^e?&Rr2b6PEsxn`~t&3E?6QoBSox6Kk|qMjft9kjyGVxUSIT6-DMwl-1h+bQcz+R!*^#EFa}@Vb@iE<A#;'
    'cg?P$hcK-_+|lF*c!9EXNov2-#^HUemE^1u+=P3fQ?fC{cxWwRWlbxx<Y>Gw(^cAc<UphKfao=kMhfzpG5ymlXb>CnBT7`S6-6!@'
    'gp0L$cD%|qT$uIu>B8EjTG^z}2Ftv+1~Xks0p&&x#Lk6mwYY+oEN#;XQsv@c%V`gqt4=U3<Q&-X9Y1-A=GB>pj%6FvD$J$&YC}|j'
    'EGV>Vt7s_P3BA&@)1uAk^}W)~%_)fC<@(Ica^bPugE^OqjkAm8baGokXq=Q?ONraoM#iNA$z<G3;i_orz3W(aZWGtI7qeJ&APhN^'
    '6lP6xDR4s>iwpJOmM8#R$BsFxR7zu^l3cT6P})$DqVS#B6J?!w(F8~|%W;&K{Oj8Vht&jv2NT5;3QFP@Rxa1umz=S@-ocCBm<q|_'
    'ivso!ljuU*Qg)jK;zO^#8gfHfv4#S=vw<?NHjTQH69^5RFokiO!y-*ll0|Pi#X6L5380>mtpwWNlfXsN;VE!p^(N8Gq9M1ZFjkg#'
    'rAWMF##{ugY)!a@D!s6{$CHXzQPR~ar5<W^w{hmXP@m3Z09^iH<JLJ<$vd1BeZe*qKOBCl>HM-&Vn9!Z54FuT1uM4kXbXk>3R=^='
    'S<*~~<9Yv+wa|gJKz^|p6a%x!VtGET<LVprlbn)$en}kds(rSOIMa~??$s<4g77I9YU9ng6347%P;!Au3a5ix7^lM1UL@;4%h)q5'
    'Lz<u$sXGzQmPa^}izs#KK+S?-D)N@%0+kuzP0DOieiKKx`DN)_jsXPTv~qnqXYehTe7=}SoP=7#P#7+X#veFAS8KIILMLs<6#|Pj'
    's>b_YQCkdtSz4h?uW5^m>p^dP7SLt#`&g^3M2#r!QB1tr)(I-~g@nF_9R<NIs(_xI4Zt!(VwubB=V~F9jyx2{IL?*#VP&v7f_O<('
    'vXKz`cgZnRpbo4a@J{2#vL&+r$~<Z52aRw*M1mUK$qhh_E@DVCFba#MNr)x=&@c>|jC)_;<1oC&$H53IOc|E9_&N-B*~|%=UTt-W'
    'VcXM7HWb7n*C&Rde3l3=PPtS$G?ad1t|*~$tAaVouLUA;Akw6Ql9)|1(W**6B0`HozvMo3R+X99U2N$)4x1i8G;wuxy$M?#J7YW~'
    'US5Pee^5u|hdy0lG*%{MHyNuiSM)*mUE14j6C2K}CypRO=;|I{LKkk6#4cN6)xg8yjGCRImq-z!tn_GCiF~$$Db_`(QFQ4nFtME4'
    'JZyRZXl7jZ()&pq@rhC(TFysRL=-hcqh+;YC)ydgk~bn6LMx(J0!S+o<qx9X>lW$8=oM1Y3LXD0es9;BW}>$;^eWhXcBfeG_NW)u'
    'G4UP>2Eux}UGU12DzV~00~{chzjAA>qrF2-4a;L1&CX5~U~FK*K)3{TxX)<51mGsx8aYnho+-7sY{MQkuAZwe5vn30j`VFh<%H@B'
    'Db)`6sIj<nLhU!9#Zp)#i!eFQE>kI%J480kWgo%Tu&|Qwvj{lH1`30m3gWgEg=yBW4A^$*-17xW)vUic>8o6zwvLITxdO0`-CAfR'
    'p+=+<{?x5ii^U;ebgqrkk-b@<bqf&W6!lB!w&~ov1?+&3DxnRur3VFadhIq)%}KMol@1h)o^_-)h~Ok{(g-S4!c)e@f|d=bBs)>5'
    '1^+*>C(`vhGSLTeT2X;%P{o%ZSY-(Zdp-Rge51CT(NpZm*Gh)=0)MwrJn6Z%)w(9cy0H<@S$+U>rBu4W3a#giLcQn#^uwBzxG(7*'
    '*&qqTiA37a!(t!(D5flU#wDp4dF8N5G-c(mR!w5c_nZ}eZ0&;BxC?X(BEE+-F}*-j))ES&=j`|_w@31*hywqygbxe!e%#&Memwq@'
    'vp{=am&Q(DY6JVVc{^A9C%eWLUV$^-tg?wPp|?wfM*#SPA7un+U~j#{f~_;_;~=kkwO@iDmkanZEsk^nJYZzS5vi_-CK>E=p_~lo'
    'xnF|!osy(BFB7&|C1@i)6^OO?>BW1x=!EJB0>=J-UMw$)mVObl<cU#<ZPbS-B^7{C2Q^o^S!CQlbU~cJ939`4mHNPS^Yh?cx1G;@'
    '@+cQtCsn_!s#brrd1&fNoUE6mbRZg_*7#r<k`V1%%v57NmrB*;Z6FF=JhU}JhRS3xG^7$mq@7ToUHV!mInbID%QDhwQc=8)SBZTp'
    't)q&M#H;H=9ee@dY_1*>-GVrYC91)spInMsNY$%0aaP;Pf&(!=MdAmq#!J)AJBeu_<x>Row4}rz)LSRca3+KYv7Jl~4z;Y7I#t7+'
    'q-vP4XTd&XU4*~9y&ZP;WrBp%;qbE%`h%h{MED8p=S8CVGHfN2mJH>(<Z4y;BLzv(rXrC2k4h?^fXQBx<k513=oolN8Py!;hcXWz'
    '*_`;CpaG$`V*X>qw9P6Rmpx0thD1E>^w1LE%J7?XvyRzTPYCYDmOH)yo4p;|yEqB9_tJH^G|E*OyKBPbfcO@LYkc@ATj<urzp}M%'
    'K_j7hL0;2#AS&BodcSR)xdwBgwib)wv(n%t&Q;(qSTqIOmsA4MHhv}k72@5+?oQxtvx*@(uw-;Bx&_%oDKp)?DU=(y%KeA}7lrAF'
    'Ci(?~n$~#P!Bh0^!=F8$R?$5nWgV%lUC}ExE1VGOBh#ofh<0dyQq#P$y(=%g=jCQkTY^)F>JKY|+g1RAv@Z6B6);oMJECVJYG&`}'
    'H3{buu<;TD2RKax%CM>MA~#tpxI^$yRb5jXXD>gBwWtv6P*G%zk*yZh*9LT^3Pn?|ILZ)G_I`W%XlQmo5%ksGaBTHPP;uY3Fuj-('
    'Si}$yVa%2;aKJHqJ_18nWMmZ@za`5@OFSX7*OR8s=MbD;V_c*W1zDvU*e$0C)vaS3=`;oLfvx+Wi&p;Ans=!?sqT}l21@gv)-OUW'
    'iA3bAn@|^iQ`=NF6^-6~j&Dy}#VC8Z51k1@HdMb!>q<xEySVskv*Hu!^Ty~hv@}mpjb2{!Db+?#roWIK%zHxT)uClQC#}!*KGznT'
    '{f`ps)cLO3_*x7TjRG}Ezg^g<>n4&<$Z)66*nZ~&wt2~*rY>@t#1nfkg^G-5bs2!|71&f-%jHC$94QPG{2d&4u|0saU*kQ<!iLD='
    'IhsiYt4v{zY&Z_(hr-c7C5Mih%`S0Zu3nYuwHWQrnLWc4`5~kw7_^p-Ir?4DXEm%D_2~|*d0r|_CBsM2rqqcj$$HI--W139qheDA'
    '_vYj@sUT8?mhyZ83NmHrQLx33lqlpARq|cv;G;t5*%Ci3pyMi^>1;_ED-c6+uuT9XhYbBt3)ZeA$pu!_zzS_tL)?)DGI&v>-U4}j'
    '{j?Z7dfy!(!dqO*+=vWbe!JSo4J(mfHR*0CZRressJT3{p|fF`P$dC<>GHSbm{b6vvj9t;NyV|fSl&Ru=vd8Ro>C>`>uS_0X+s2q'
    'OEkL4IJ2#wE~g-vh;ed!8!w>G-k=#-ycK{5htH;pDt{8n#*#ufDPIh-gfu#Lp^nsm8T!a~ICVksG7Xza7j&iK(O}GWe}~K(B8$zo'
    'xV}wLZQ)L&Ud2**&qigcNMf;DZVpk@k|5sev@*-H&$ZQhbb}gz(-<3oWCzqJ%Q*gMRrQ29Dg)zOPCFL+1VqHjU7Z6Xt4q_9CJqpT'
    'DWupW&u(;8(Ks`1l0ZQ0wU~Cn6~QX9(rT5k;z*{aP;Ga|2T1u=j0Lv1{qbT`rkF0<2Yy^2h`o8}xhRp_&qUbd_LL3X{%jw;@TH+6'
    'k0M3b>S^`h_1T#*IrY6S%eGez-rCS-Fiu~othL7^TbnG&W)UXY?;SAW$Wd?l*mtR!wF((a-<2d*dM3WVv6KLoL>Q~jV;Q~}EB|9;'
    'F|Iw6AhayCtr(Umy(g(kl-^d&XNs+BT35WS9bF(x;E1szHn)w=6l0}@4A9cRS-tu()R9vg{%r*mfUk?xOH-stiLgwAR9PfCBuLGX'
    'HDPh9Bjw*!--=MdkRqO*>C6g2rM{m-KEw2KsBTCLYJ(0>IqiSO6-r=)a-xJVjwCRvCUwQ?^4RN#(W11?#lBVQONW~U3v3RH>ZhAf'
    'uvIQXo_0N?QhP=s^2tC%vakiQGKP)C(V}#sj~lqpR3kw$s#`?F7wIAlk^pa<E+xgzv5L@7W_<v%fgjF3q}Cx&d7}e%`WR}KpR?9d'
    'Jh_mHBoOF=?u4uzB|szd*qPcg!?rZk+W-huc7m>Dx(2SUoK_*LUfe7XYO~5!uNTp&zj`@3^(Thj(&|=ajq;AvEJ$a{AZk#Ut24S*'
    'Ks$zN><(3zO8sJ^6c%xz(wgyf;EB#3t=JeqXgRN;ZMclM6|h3sCZQNvDqL!6R|tbH4tNDMR|&=DlKwJ0Su8Um7aReaN=TbaDSjoC'
    'M4l-npfUYn(P%9NRdsG#4}#vXI5!Zyld5!W&aquLng+d*3<yv2G9|Nu{2BmtqducGoF?oSUajS#_NPo%&P;^XXXJ=R$!<vgifa6#'
    'kS=HTj3P9l2T|xdz>uh99~-+KD|5w#sFfuH_2Nhij<{m%GQCW%$TAE>X)+|DJj&0%ie3J|gGi`3Gu%biTAB%Gm3J6PSQ7qBjq@Xg'
    '_^xVFoh6&C=7UT$dw3D;GP;cF?2j2FiqFV`9`C3#iwr%Fa7pWnY?aUG#O>)bjJ#BxIW8yWIG3j?E4rnjs#z=0xhYp`tg;TWnFvW+'
    'Hz7UWjw$vH!6}vEdOE>%JA>pH7e$wp`WTH^yBwsX^o**Hu@Hk=Ta9)6^TD&q{EX<+sqi9Jl}5FjG79igk)KsZcIYBhVM{EsYyeVn'
    'WG6xgpu{`i>*n?>kFWd<taVvbG|h^f7Hc|=`RmnfRH-YA5*pzKyMMzNONJ%f!z5X4$f`%FdLUo<Nawq>A&_xUy;Fb-M~4WdC1f|n'
    'UQ#-a&_KEscqfS(QiIHj9~%mQlp2BU+YD_U!(g<b95vN;iZ?Pq^r8|Zt=Sjjg{X6G>`o_RVw5D0KFwl%k`3S5cxt0E6W~s=(KnT;'
    'BU7Z$Jk!}PLlJ;>WifRBiBv_(fjFH(DgxD=knuwX4p9d3HRn(@>nt>YUSCqU<fso@(=G%sqX4@ySYJp{l$~I@c`sy>Z2>~#?fe#G'
    '#O}64J0>PpYB(h#eqf<L2@hxkyZZLBj57?CsD%LE4NJ3bmW<t3!iG%0h;T#ZEQ@M%Qp?NZySy`@>hUIG$c%aM%`7FN<|$=b-1-ht'
    '7j8!&psM#IWm+{M-In_NJzxwDsq!PM*!$Zi=ZH(o3(+JJQjjzPZ+!ZboJ%cxpdj3l(!-2;9N&WE|LigeVikC@7uGH%4?Ij;s_%8D'
    'AX9OsyCu>rSNpgTj4mKi8{7AP{fGYt*z9i?'
)
_ROUTE = json.loads(zlib.decompress(base64.b85decode(_ROUTE_B85)).decode("utf-8"))
_SELLABLE = (
    "STRAWBERRY",
    "MELON",
    "MILK",
    "WOOL",
    "EGG",
    "TOMATO",
    "CARROT",
    "WHEAT",
    "FERTILIZER",
)
_PREMIUM = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_ANIMAL_PRODUCT = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG"}
_GLUT_RISK = {
    "MELON": 3.6,
    "WOOL": 3.2,
    "STRAWBERRY": 2.0,
    "MILK": 2.0,
    "EGG": 1.5,
    "TOMATO": 1.3,
    "CARROT": 1.0,
    "WHEAT": 1.0,
    "FERTILIZER": 1.0,
}
_REPAIR = {0: {}, 1: {}}
_CLONE_STREAK = {0: 0, 1: 0}
_LAST_STEP = {0: -1, 1: -1}
_REPLAY_WINDOW = 8


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if 0 <= seat < len(farms) else {}


def _action_at(step):
    step = min(max(0, int(step)), len(_ROUTE) - 1)
    raw = copy.deepcopy(_ROUTE[step] or {})
    return {
        "farmer": list(raw.get("farmer") or ["PASS"]),
        "hands": [list(item or ["PASS"]) for item in (raw.get("hands") or [])],
        "market": [list(item) for item in (raw.get("market") or [])],
    }


def _align_hands(action, obs):
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
    action["hands"] = [list(item or ["PASS"]) for item in hands[:expected]]
    action["farmer"] = list(action.get("farmer") or ["PASS"])
    action["market"] = [list(item) for item in (action.get("market") or [])][:10]
    return action


def _position(value):
    try:
        return int(value[0]), int(value[1])
    except (IndexError, TypeError, ValueError):
        return -1, -1


def _tile_at(farm, position):
    try:
        x, y = _position(position)
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError):
        return "LOCKED"


def _route_actor(step, actor):
    trace = _action_at(step)
    if actor == "farmer":
        return trace["farmer"]
    hands = trace["hands"]
    return list(hands[actor] if 0 <= actor < len(hands) else ["PASS"])


def _repair_weed(obs, action, step):
    """Clear visible weeds and replay only the delayed actor for a bounded window."""
    seat = _seat(obs)
    if step == 0 or step < _LAST_STEP[seat]:
        _REPAIR[seat] = {}
    _LAST_STEP[seat] = step
    active = _REPAIR[seat]
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    actions = [action["farmer"], *list(action.get("hands") or [])]

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else actor + 1
        if index >= len(actions):
            active.pop(actor, None)
            continue
        age = step - transaction["start"]
        if age == 1:
            actions[index] = list(transaction["intended"])
        elif 2 <= age <= _REPLAY_WINDOW + 1:
            actions[index] = _route_actor(step - 1, actor)
        else:
            active.pop(actor, None)

    for index, (position, intended) in enumerate(zip(positions, actions)):
        actor = "farmer" if index == 0 else index - 1
        if actor in active or not intended or intended[0] not in {"PLANT", "BUILD_PASTURE", "BUILD_COOP"}:
            continue
        tile = _tile_at(farm, position)
        if isinstance(tile, dict) and tile.get("kind") == "WEED":
            active[actor] = {"start": step, "intended": list(intended)}
            actions[index] = ["DIG"]

    action["farmer"] = actions[0] if actions else ["PASS"]
    action["hands"] = actions[1:]
    return _align_hands(action, obs)


def _shed_access(farm):
    size = len(_get(farm, "tiles", []) or []) or 10
    half = size // 2
    return {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def _plain_inventory(value):
    return {str(key): max(0, int(item or 0)) for key, item in dict(value or {}).items()}


def _projected_shed(obs, action):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    private = _get(obs, "private", {}) or {}
    projected = _plain_inventory(_get(private, "shed", {}) or {})
    inventories = list(_get(private, "inventories", []) or [])
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    access = _shed_access(farm)

    for index, field_action in enumerate(actions):
        if index >= len(inventories) or index >= len(positions) or not field_action:
            continue
        if _position(positions[index]) not in access:
            continue
        inventory = _plain_inventory(inventories[index])
        if field_action[0] == "DROP":
            deposits = inventory.items()
        elif field_action[0] == "PLACE" and len(field_action) >= 2 and field_action[1] in _SELLABLE:
            requested = int(field_action[2]) if len(field_action) >= 3 else 1
            deposits = ((field_action[1], min(max(0, requested), inventory.get(field_action[1], 0))),)
        else:
            continue
        for item, quantity in deposits:
            room = max(0, 100 - sum(projected.values()))
            amount = min(room, max(0, int(quantity or 0)))
            if amount:
                projected[item] = projected.get(item, 0) + amount
    return projected


def _safe_market(obs, action):
    remaining = _projected_shed(obs, action)
    market = []
    for raw in action.get("market", []) or []:
        order = list(raw)
        if len(order) >= 3 and order[0] == "SELL":
            item = str(order[1])
            quantity = min(max(0, int(order[2] or 0)), remaining.get(item, 0))
            if quantity <= 0:
                continue
            order[2] = quantity
            remaining[item] -= quantity
        market.append(order)
    action["market"] = market[:10]
    return action


def _production_signature(farm):
    counts = {}
    for row in (_get(farm, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            for key in (tile.get("crop"), tile.get("animal"), tile.get("kind")):
                if key:
                    counts[str(key)] = counts.get(str(key), 0) + 1
    return (
        len(_get(farm, "hands", []) or []),
        tuple(sorted(_get(farm, "unlocked_quadrants", []) or [])),
        counts,
    )


def _clone_like(obs, step):
    seat = _seat(obs)
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2 or step < 96:
        _CLONE_STREAK[seat] = 0
        return False
    ours = _production_signature(farms[seat])
    theirs = _production_signature(farms[1 - seat])
    keys = set(ours[2]) | set(theirs[2])
    distance = sum(abs(ours[2].get(key, 0) - theirs[2].get(key, 0)) for key in keys)
    similar = ours[:2] == theirs[:2] and distance <= 2
    _CLONE_STREAK[seat] = _CLONE_STREAK[seat] + 1 if similar else 0
    return _CLONE_STREAK[seat] >= 12


def _opponent_exposure(obs):
    seat = _seat(obs)
    opponent = _farm(obs, 1 - seat)
    exposure = {item: 0.0 for item in _SELLABLE}
    for row in (_get(opponent, "tiles", []) or []):
        for tile in row if isinstance(row, list) else [row]:
            if not isinstance(tile, dict):
                continue
            crop = str(tile.get("crop", "")).upper()
            if crop in exposure:
                exposure[crop] += max(1.0, float(tile.get("yield_units", 0) or 0))
            product = _ANIMAL_PRODUCT.get(str(tile.get("animal", "")).upper())
            if product:
                exposure[product] += 1.0 + max(0.0, float(tile.get("yield_units", 0) or 0))
            if tile.get("fertilizer_available", False):
                exposure["FERTILIZER"] += 1.0
    return exposure


def _clone_front_run(obs, action, step):
    if step >= 717 or not _clone_like(obs, step):
        return action
    market = list(action.get("market") or [])
    # A front-run is optional; the scheduled route is not.  In particular,
    # prepending to a full market would silently evict its final order, which
    # may be a HIRE or BUY needed by later field actions.
    if len(market) >= 10:
        return action
    next_action = _action_at(step + 1)
    next_sales = [
        order
        for order in next_action["market"]
        if len(order) >= 3 and order[0] == "SELL" and order[1] in _PREMIUM
    ]
    if not next_sales:
        return action
    projected = _projected_shed(obs, action)
    already = {
        order[1]
        for order in market
        if len(order) >= 3 and order[0] == "SELL"
    }
    for order in next_sales:
        item = order[1]
        available = projected.get(item, 0)
        if item in already or available <= 0:
            continue
        quantity = min(int(order[2]), available)
        action["market"] = [["SELL", item, quantity], *market]
        break
    return action


def _collision_order(obs, action):
    market = list(action.get("market") or [])
    sells = [order for order in market if len(order) >= 3 and order[0] == "SELL"]
    if len(sells) < 2:
        return action
    exposure = _opponent_exposure(obs)
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    sells.sort(
        key=lambda order: (
            exposure.get(order[1], 0.0) * _GLUT_RISK.get(order[1], 1.0),
            float(prices.get(order[1], 1) or 1),
            int(order[2]),
        ),
        reverse=True,
    )
    sell_ids = {id(order) for order in sells}
    action["market"] = [*sells, *(order for order in market if id(order) not in sell_ids)][:10]
    return action


def _terminal_liquidation(obs, action, step):
    if step < 717:
        return action
    seat = _seat(obs)
    farm = _farm(obs, seat)
    private = _get(obs, "private", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    field_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    access = _shed_access(farm)
    if step == 718:
        for index, inventory in enumerate(inventories[: len(field_actions)]):
            carried = sum(_plain_inventory(inventory).get(item, 0) for item in _SELLABLE)
            if carried and index < len(positions) and _position(positions[index]) in access:
                field_actions[index] = ["DROP"]
        action["farmer"] = field_actions[0]
        action["hands"] = field_actions[1:]
        shed = _projected_shed(obs, action)
        prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
        exposure = _opponent_exposure(obs)
        rows = []
        for index, item in enumerate(_SELLABLE):
            quantity = shed.get(item, 0)
            if quantity <= 0:
                continue
            risk = (1.0 + exposure.get(item, 0.0)) * _GLUT_RISK.get(item, 1.0)
            value = max(1.0, float(prices.get(item, 1) or 1)) * math.log1p(quantity)
            rows.append((risk * value, -index, item, quantity))
        rows.sort(reverse=True)
        action["market"] = [["SELL", item, quantity] for _, _, item, quantity in rows[:10]]
    return action


def agent(obs, config=None):
    """Return a deterministic action from the economic route and visible state."""
    try:
        farms = list(_get(obs, "farms", []) or [])
        seat = _seat(obs)
        if len(farms) < 2 or not 0 <= seat < len(farms):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(_ROUTE) - 1)
        action = _align_hands(_action_at(step), obs)
        action = _repair_weed(obs, action, step)
        action = _safe_market(obs, action)
        action = _clone_front_run(obs, action, step)
        action = _collision_order(obs, action)
        action = _terminal_liquidation(obs, action, step)
        return _align_hands(_safe_market(obs, action), obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }
