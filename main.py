"""Kaggriculture V4: public-demand-routed mixed-farm execution control.

The deterministic policy selects between 10C/4S and 6C/8S public-replay
consensus routes at step 168 from the first two unlocked town shops.  It adds
bounded weed/cow-placement recovery, route-aware partial-purchase repair,
quantity-conserving H1/H7 sale leads, and an evidence-gated second-order
counter.  See THIRD_PARTY_NOTICES.md for provenance and modifications.
"""
import base64
import copy
import json
import math
import zlib


_LOW_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>Z1oa{Mnm^Pp~aH%Z?(Qm-W}XDCqAHr4}TFo4%EV5|>g-;Dk5){^~ERWC9!GV>M58R*t(wyNIu%Z!YS{Q3XR{^Qr*{{FY$&i>`+vmd^Gy8ZCW=bJANU+=ePkLPFq`RjlG`~Q6V%eRkz|Mj>3`rH40`~36S$4^gx)js_2^{>C&{PgL^o7=PVv-fwqv-4&1^_P#^?dQQCzHGN2zJ0y>xV?EeJHMQK{p0rb?x(Z!#qsB#@9#c*egAO!ADhR=f1D3H_W9HMKY#svdedUix1Y~;+b<7KZT;!){^8@(r{h<X595LOvc0`Mz4c=H*2CiluL2DjzV`HKIu)n^lh>KE2YYyI$<v%HMt$A?ioEOd?alkGHJ+$HhyMWHHfc9`>;AtC$Fph2(|13e7Q?8o`<XI+=8o|8X8Qiq^0;}}-cJ|N^t<uuflGHeT|{5*zD^fWyEy;!&z&*)X3{%0mF?h+2Y50{r~bXa*)Pq*kDhntpzEQzJPlX-(!(eWf8|aW*nenpz)omZFnP;<?7^4~hNGFW_BZ;B?Z=%C-RQZ~op&0-cAAWJxeyLFuo=vwm7gu6E@&f*4jq5;4lUKkQvSxDM=*r@69&wYH*fkN9^Y~N@a^pVf<D9s?lkU|2k(DLC%y0U>4bObz~TQ6-qiKE?uS=+?BrItFsw=EFb!NFeV#f!TO-@|#al47N61ebGonum-rwEcZr?xr@~7?n!>8L%|294oIt^a>C4nW9e#cC6aJaPx?J@Vz(Gi*a*tp8qj{yttO|SpJ{7(D0%6qr2{a3U}fO*%Lj{_qdEZmHr0gMs2CvdO!OFLvH^F9oF>-EtcK;YO13{vK*z)#)-*;t@Y?gN=eAli=wf7EVr(t)xERkD4R4Mcr&fBuQ5Q*(V4;K_X)^p*q812FDSk8F)WfAhD%39&8x_JtnjnyLghdtt-+`_uYAO}_Vm4Yg81?z~|@ZH2aX2v1*3@bPcQ-~AneY@~CM-MOG~${b`&i(@+mXW15e{jsY>?qA0N2n{>}<}KVHdCAZVyUQ>moRy-2mBHl36T?6Cw^FkQ^%0D0Y27jlq5WH*;RKuT1W?9b#h^E52op0Fx<_6Onfv~t?=SlPqCe`3bX2j2{b|!7Ag{v30oP$v%iu}0?`~iP=3{H1SJIUafLyhxuxEK@kf|6{7->JDI#kgGX51KK^YP~XFILC;*){<PN2C^@p*r>@IYh&;sPI18!D$1-M}|iU-Qt6O?AY^LV}p*2#p9q1N6N>j0O&PZcBeIZ7?e{OS|0S%6Vc@}d>?R)^r-)VI74r^jPnHsseN$EUHijExxYX5#TW$Zh~>0?+VdlN<`rh6E+VGY-iZ0~aDTJ=VS9i7S76DcU_Ztyy`pc2+}LGz=#MqfXvE@i1|0AO!M@Pl889QK0AKblwGopnR5zE2HMCBKSX>Nm<6u!~eH=d=uXO)$8V-55kq4U=Gm<;TpG)4!bOe&C!0LDC>*r=>Ekg9^xuKc3cYDhb7NS6)k33E={34I5aU{P-8(%ASxd~f91-s_rF>!oSgh8?qh@paxSH+p8zPbm-WUdv4Rtzq|-QC^oQ?3#;t@eN1PtdpX@xxi#);sz0xVM3?rK3|b2N`dr6Om{-)Yh#a8@%IL39sejM2MgqjO$+tlq`@w*4t1>O%d}$?6_a%zLsF95@%2MU22rIHoEH~WfFSZd`jb;TPtZL)<giCP6N-eCL)w^Kx7+ddz5!Up!4l?qoZ$nT4c5X8)o!L9~5xvv;gunpD9Pf13t;byq(L6+5}UW7paKdI5xKOEiafx95%;99-HRq%Hb`*AkhI4lu`{+fQ>eQ>z7?;I$ELl)7}6XU$-~8@k0(N80W=BWU^rzwVyK|vk;_vo2E%p0-XyfFo5hBSqh+iVE%8MG<U}4KL(#jnz=)It5^?g2T^{Xp5)IGi^D4r{)eIgY*PNuop@x63i`J!@gdlLYu8IJ+pG;aPgfTF;Ey!3Cyu=U27qa6gvPn;GJCGsznIBGL2lB)Ch!bWqcclec_kYS1mh;pIi&?)%oAr@WSkAy8VrBtkOc!8W30x8pXn?d9;vh>gI7}?ft-c^3JLmsklaPs2dT3Fud%lgQY{)13R{~1{w(BqBywuN?OHR~IwfEpudE>&Y?=PRs3Xptm8y}Eap4SAZpdP~QZ}*1ObUrzpvNgcn7}`Ny8ZKhEn1#a`%6C|GwjHrIoj{`=NB(TR6zpWhoPKRbkf0k3?mL4*RA-2;AO|P2~Gn+j3|_D8;np1sls#0hk?`lWWf*Z<OV}&4SkN9nA4o|Zia`8&qvi0&GfOn@Uhg^qeGHq;#$PVY0Yl~bKL?;?a7X$oLafO)?Q79V_QZoyLR|qv5j}1og0Io!8^6D%)jOQ7Re`0e8>s}cwUp~w)JWq*#>m>V$QDK9=77ah1L38eTN553q@Vri6s7F=VjKuphbJ8UiyoreQKE0i{-R6CpJ0EE3KL%_qTg{q%5?0tWe^dFH5=-f`h)YP89w-;-WOtVsp6g!2a+&ctYWgML%_i-t}aeIU{CK`uUW;=?`;_u(>JwwxRUGN}?w7?Azsh3UjqT(%}Z3(4z}vKQqQwcqM_<LkS9^ZbX{QH{!Uh2-4ts=)-$vJPHa9M4jSr<d?{{?;92InB{~LwDmRpl|cLmaMBtF88ifWrjB4sYyM`qe$I=f=spR5PX5$~E(K1VCbo`-7VJ!0#GE~~>Pl<FO0`zB=~rPCKxZPkskSbbYA;ecsh`L~oCe6eNCe6h13IC3_Y!W0GMO`dC{E)Gv?_n<yoEsoCfHkO*7w2szCGuGC}ih9?fZfPHg6`h-nNZ~)`hTk%-2QT(Cu9%$}YE(1w=BDq|3*eLUl5K3z+^Y4<d)Ir<~9ji=6sU8O|FZNYdaFkK3V#l(hvQ;lj4b&z0n%awVnKCuX2GZ7sv3a&yW3+TmNopldaoi$9v3H@Ml>!gR6Q>ww4W<gqdWFcJ(U%gw;keH)9oyJ#yq8wigzOhN?hUA%itFl-sR*Zv6L3#YGO^c^?#s*P2w{7Z_4QQ;}YP>8J}G$A*CZ332yg}>(6I#NV%!MrdWPwv&`F~b8O&=|<RI<Vh{Wi|V)uF+$i&b9kxl&wjcNz+>ig^$FdOI=&ot8pFJXVN{+M~2H1l5V5kdCT=8u+zw_AkFtCV(pppa9BX5v)tkJV@JU$no$MOVY3V;n!`5MovQ|53oV^<y(2^uqve96HUk#H*1b-wwa_FSpf=li+5Q?zbtngJNH}kL)T68jw37zpYLZWV)H%uKP>;m%(zy*Bm3iGfhnByoyU(tJZu*j)xDy~kD-@y*VHwfDzkuIdMZ`tgKpx~Ycb}oER?aDL0#?gLUuNpIjm}j4nlx8^E-8mmj=X_qiHJ5cqni2J#-ZbU8*W=nXp<TG0dNqH9q@)#<4&`?x{{@34Z>ES#@82wdG2UdgjNBLCnSJ=p@+E2mZfDw*bp>*<}I!mW)ssrY$9fIb%jL$HDJm}+#n7t3SSS^&e4!M$moJ?zwnava4krYVT;QWFLOx91lM*uplGld58+2f)^~^rn<*+~J{m%LSC%-_)~~gwSoiz{tE^~>yJ)ng(&7!_m9mUv*Kuh$4fA7T9=^j^K+JtSZLi$HlJd2FqKLyB>q(L|T4>c21PRR3ixraU#ubbMHYaeVE<n)}b2)xFY|oVg(aev*0LFtFEHxqEoE55PrQ{hhBKD%lPrM5zsZjek?x=%ke@J?uT>we0QC*0+s`bQHkdB3bm?&rN_z||0iZT_MP^*l};pd3=5v}=*y!3Py6`OW9`-TxITtBZyx>tn214%0ZLz?V)acJ1yXsHp!>>kGIs`$M^4roBAkmw8#ydBaNSo5x;1AsXycBB&LNKW$j+(A>Lf{f^-1z6dTPga4X)vT=nRw9B?t1!<*Y5e4v?FmmX&phr#7^0j>CLF7l%H4W>UD$q{u9{uIt>ccqfMO&@nkk*+!3afns=O4$;iCGH*mV|#0u%;k+`DI_hiON<OgM^}S>y_-z-D0tO9~a=+^=)u^ADp=zYBN&#W)wOH4iNbDRIEYC=y<OYl~!g1yR9=s)W0mQGrY`nNX37LIR6F>F>KvR%SAaKoOIgpng}pP^cb-)YL9?pVd}|OM?3Dt6P4?PI539tx$Ie5k%J}Ho2YP+)j&V3Z#aMQV^8)CDosgD4vWjn}i~SBd8$Bwn+5SARU=44<5&lX+^kgT|Fj>&(o7%j9#+culcm>P@td-<#^DPskHws>47)_b+#DHR1*RD5X@{X505SezR<I64brPxFF|$1<F58naIxC<P`9f6(26d0XejlpiMpetS=hrhTn4fal8k&du%d^U&op3Duhf0;mrj=<CgUhAUVYv4Xl^w}Bc@1NTM;>y!1dc>3GmDebn|zF1Tb<9l=B-*qf|E)ICh?$4}%^B7kU>A+}CSFl=2#qKD=JIqAc`4oOQ}5*GJ2UXP?V_4VJ5rDe>XLPAY9+kt!9#(1rsCy+u%u--L#F^H|AGiFs+ET?>*mG`4-9(gT?dsr-PkPR28lp&GP9ej1MP(}nDg9Qb9|=*u|Z8E%TCb5kppt)>Bqa+#T_W*Q-IAvt7(Oy(dh`R9qzP#{qRIF`8+T}pcjOT1i!qHnrZk4Qb%*j-9FR7abqK(tv!9DM36+l-qST=uM+yjU52z-0vL;T*j{x<okLK%!6pz>B$TFPC8ddx_m%cJazyG;|v)4pzv8pCO1Fs2WIaPKT4NuvxsJ#ZEJ|4T?l<5UI;E;vF3^p5R`jX}7CoT)*&HbtB+)>*@MT_+;?zVgN{9+kpZCQmyO?p%mF8R6o@drSnFiRCUT1W@z=$s2@UUvei8RB0hTFfeU(tOE2p3UDSrxw4j_wQ`U%76!65Tt2BOHLa~yZVr-xt9(bJ+O;$%lEYpd?QciW()gh@GgghYrD0Sd3ixg>|E5@WB?Fg{Y=<~9#qB+Dg`p-PWs7HTYY&*3iDH4*VR9{>1vh#_{yXoCG5}HK(sNqn2`1G%lJ}#EM+m89;&sBs68f+WuI<pp?-<9=XVwzV8-Zpe^B&EfZ%WqU*hu`28TwR<-QO`rOokEMlHUYjmB4TVkszM~<v{o}jTI{HMVm%y-m}u`D7|#f_T`0u;#lqMb%eNYu&k^`bL3*xkZkpo#V)I@C?lvqISf%2-CCG!Sw)2GN<E1H+l@Lqf3)J_UrTRu|k$PoGLnP%SU!KK_Jny?xK@V?10h?G#C{JdxYh-L*L2}!p@;P%PF^uJ~9rP)o{hWw2Z+wfN+|kE})Y8;hMwcc(lGGZI!oX+&g&7g37gTeAZEf!7mm=o~&kO*-G)nAEB?&ghVkc}D62(fw8rRufc@Ki+W~hO90$dxQRN6xT=bA<D@T(&AZ!yy9lR_43@q`I;7ZDFq0t8sJ9)M|m$RRN?Nv<tnawWQX>8wg5LsmEwBJ8s+Mcgqf{J){zYTJ}I!(jld?N{Y20KY;eEzoM%b<zSzG|i~>3krEv_ZB+(epqm;#}$jRPO=N^{avZaDHbTqyU$rww|0rO1lc%8z-PAhD49nk(|57(MSL|fmfodx@V<*Ax;jc+o}`oGOBR?vibfiuw+BEr>d1I&QkP2d9U!WV8;ad<;DP)#S(#5qDfsH4ib`QEfKb)9M6Nx;Gt81yn;9p_t>hNb+yqVt3Ey)}$BRs9M3?=u*ZNM97GRK4B2<736;Zqfg$6}0gU~lbc><p5!uF$lP^<*+P6WSbLKOHtBhVxo4j~_nQ=yfd*7imu#X%@5>X%DCw$!@R;g1>mEVmz4O3iK#TD*{8FXL`|W<qJcKz}bAdWsZ0cZ=b8oEo-dO#%q@MZFF;Pg4v37El=)B4ehNT4X5$h?&bE*GHc65XvNCq#3CoQe!8m@X~};;_5RPHA@>KMWnp8Y?2`1)#;M4gjbz1h?Xm3pMf&R%Qu!<^oFWHaHt8=s!)$E+^9p(T%)cKQUK>Gl--nzMRY7YDU4H&xgaGishk%rTSP$6W+^qmAQ`=2rCj$z)2BNgYo)w#33!obN1}%wy+Pfp1p$RjY&5hN5<Q?POH3qzdVp$;#YEvs+W{UYoZ<nNc}LCll1oQol`J&xI4-fOX%G;^0z{X1c9E(q8rFti2J(@3!!&sbmA?{iI9VfVav$h{mJOV4G+86#pakA*vW|4uWQBEvt`e(>(*8{q#+CiecWF#Tt5Tx2oUtDUaLhlKaKBE8sDPmnr14SM96qn^ZqyUD@c7|LD;uy<i|Ji+CFm?FsZ-Qr=V~#kx(951R*{pcmNL=EEdk)xokcJ$Xl|YEc2+7=$w-R!?xKNJR~`G6sq?9Pn70;alS(v6J9<4}=yY|yjq)H4UyIXcn@p+6k=Pjt8X-Lu3YU^dmE>^oM`NokLgEsA^&FcEwzC6;D~Sa;wNJ%hry`)}<sW%?0u4vF&{2+`ws_3wH4>*dkpC6LiIiD8FJx7Kl%ZBTOUm0qrb%mybM|B)036_kxdnJ6{Tt4S&|pXq&egPebNnz~{h@W{aR{4gUTd-!)9wc-I+8mmI+6t?&5h6vX$_)&Sey#6&SR!Tiyd3eti3|L5gIwGExl0%JZsX#Gm+7tu;HRXfofmYr5OWwfVearianFNNQqZ1E^>3`sSO&CtIZsjO8tr1H%@nC9bC%1a4B32;Ve|p8DGy&UbNKdh$;(DVz>XFmwY}ww>putHfgCR9{12BdRTO-5B;tnWrfPiOF-jJ6A^G&X<f-^mywJ=Mjm3Re^S*%c`_AijO2#KdZVeo33+XO`W2HG(n=9gsCoMPWH;tY-+U&8tp!rp>*s35i~fvyxh}OlsX3IX3gnuG9Y|rVI+2?+sq(z$EFGK&%jT_;+^y{JPO5_Z1_hBAU^I4Zi>06(^E9EJ1U7?aWC7^G?`m0IiHQeW847B(ib|aqmQgj~Xvhhe0lYX)lVWM2?$m;_UO^6%v(FY^JD*~CCwb_i$bowVSXdWbn(hE{nNJAM6NN6$Ig=~6YS;`jw@u=>n7wE0Jx-LOy$TRbM3G{HIq5OuAbJ`u#zK)Ky5U0bUPQG!MuS%goW@Gf>TfguC4+5nMBYcp*}u?QF;~dA4_dM(UCciACbE}lvUftvi;0@MHSnx6TL9|Vcq^JuIzg6KS@#&D-0KqjZ<bWc8bqovlY-L;vAQZ1Ydmr>auY=V=g?99BOw^CSRjjXm!MUm=Hm6@F3}chX}tcy>fF6b`kbswg>MTItSV}a?&c>cl}k`pSRc6Xmzo(#s}RLT!38I2I<SLjv&vdFaVdhbxV}UXs^8T3Ab4xEet3@(Z^Dl~%QD(?mK2A%jxB7(gp+s<n;N5ErN}T2bAn}4coKP*RhMFoY*PD<-=j{UA&S}%nqe|}>s}WO6qD0>nad$oUsDMO>)h7jmB9eNTUUq?>vzwr0He&KgCN)?!L$1-w<O_Q2}Ot)`e|Hgz(o&8Mui9jEpsNYYW11pbS+oWaXV`eo`P8#Rf(NWL~C=dwaPtz!=myN9PHm0Nn0J&g&5Sqz$kG0AF7_sHE++)cf>^mFxAT^Zun{6PUZW%2ff^GxM$6a3_uMXpI5?x(eV7A9hnP(44dI+4S#D^q8|;+pgnwz??*_wOvOwU$9ZR%sZG1>vZ2k+f*sA1u~3ugQAdL+WxHr@BylM%x&t!YmT&umm1OI~lQL=K0y%qrYE+I96hQ<fB7+e`ZUwz}l2jH=UCXkkc9j%H2KOx<OMI&29J)*^8m)^$nyZqo8(U1#0?op7$oVGVLSdGkr|}i|B`+x~-lZvc3vhu#)8v+^SBn0)GO1UA^(Ll6Qm(p`2G(Up+7mE<P^qQinbQ@VBYQiwiP+L=W86fZPoQbE_rZn9dZW#C_K6=p3%gp^sYr#hRJc}{iian5(7Rmz3Zo&mYmoO-SgL(MCZ$jah?B_$3W#=BCck~1+BP0qL8(77_D2d_R#RAFWIO;dwQG~1PhP4dEvoV4#x1T5H*i_aS!JLAE9XEKBITLsXL>Rn7cZ+g)z(jsNfhwg6tb*H-9(hyD2S(P>6+4rh2*?~o0HXJq=g13x<!WL0RQH*0`=ZrL@<5oL~AM9?Nu_sgoPBzj$L0y(j*BZ5uw8aZ9oHOrkZ_Q2@$?B4&@LaI#Z722)Vv6_=qhT=sQCZZ!;&l2`&jAj_J!!<nq%}DbJWRTnBhi04-gt)-4<4df*w+d6prUCxGSuCwAmg8fEL6EA3Q}b&-)>d;;Ur5+N0$>j=gOkWvpqln_)oi6<`x6V(_@;MNpfOhDP{t=pbckxH@bsAQBF&+ltv)6>$a2}0UTfTg3&&tX@BOY2qIOS7x2ZLy|<P@9f%7y9T>NvoBGUm_Jcg5-exI$Rjm@nvWxF9NuyR*lgY5yNwxsV=Z8LZ3<{5%26_>p@3j*1h*106+b@e*Vn3=AdRQSoFz>m}_RE?)1EyQ+FFi+TjbwS5X&gY<kx@V&0DTme=?7OIB>Vka_~(lf?ZD!;GDXd37B)beK3%NET{0p%}Pj)8NaZXemhb(uk-SLlIp$j0B{dUBz1EBNllQZyj*QCgZu<k_Jdr5dPp+5}9&qjFL8AI(9{t7Z*D)Z(vBKkmOSQ{wk>ovqPlTabh)SPM~y+pwP7m%&p9y*D92r%NSp4-GQ9#W59y}zQSJ_`Nf8cGv(`OqPixdmS7<6tHCG<;q4jj>CAh7SF2wL`aD}-0}Z2FjD|uzbH7mv`k$<xK=Rz<+@^ihKNAxGf>>Oc%NICiO$@-MK&QmXZyA8fP#vZaq|OmQc=^rtKu{`3()|3y`jvDKjd7O5opa?u375D%7y>}DinUD}h~6-4u0!{gMw#v{H=5<IT886F>9#NmPAC;hsXaf%I~3(|3m?*MX$5$*>;ztO!VUL$=p%8th+kpSXw-?I3^tkrOR1NFl-ot#<?%%Qv^LU2JAP$bZFQ7<xbN()0M~X(EEJZ*X`FvC0Y#rk7wf?)PbA|LL8YGjID(6O=!Bp}geJx~>}sV7zz#Dht|8$hMKaJYfGcT~I4QBEI$7CilSBxP;66_SX=k^2f=?~pM3}`dk?}fA7dQ+rfCFDKv-Rzk19hU*%zX)z1AP&uT7-uXR6Gxt0=16%Ts6>uki0}Z>%$<MDepLBc@(OCMzJ^ROr>a&qW#pDMJ94mSY!!d`pYzV%qh|wA(go^#r@PA{jr{c(j&h$kObe}?NsR{uE(<}62`opDLPzU>SQ1p^xbS+F*<=1ul8lz5^5{01()E9iMiIapG*&IZsH~(gh_QwOc8hQmmRgq7zd2%GI|H2lh&(GQjE2?4Di3Sg~gx(A%49pRepZD?L#4JT`ZRiIe9pDCu!WEC6iWbbA%inaDtUpE~P=gOI?AO<0MFI9h`HvlI^0?eb3V_lPMdbLawHP-^ywO>pX*mm+~PHrPhBMsKD&FGz;!>jy0eajiu8(CC34n(W#fbtKV1QZZ>3FEJ$e4!X(~bMIlI?*eF`bH-uR5p7fbGcylI{m+;AJ08d_Mb*RsKu&=KF$eFhu4ZeFh(>bL2`qwlS5^t}&$@0B{3a7EtT`v6IMZ}L0hilj*msRT`*5~#PML~TsjvG$92)K$27lq{%10`Uza)3VT?OiYAlSX84QfQ=#g`(G&z~FJEyXFi>zK<|lLjAU7D5JI653n!~OJ^bJt!$Zqu;n_FnaWc!T@ig^n)})ZLDf7vR}_PwOtd>(v@Lpc@Bo8Co(Pom((*iMh2O2BtLA7k<%W?Ghv^?}YLMOb*eH^;Rtr_zrerE()o6VfR?JiNYNGhG_ZA{o<iS)0LP;I2q=%`bQOgxm+qU_6?_$B!N_U{^y7Ge^6h3zj+)%;f5;Tzk8VKOVK|;MGfKtpft-FX)hiPO`OBj(@af0QiQrygZyQZq^z)vUIY;CpKR^-iwmb%PLKQ%SZq1!ZWD%kqZ&-=XyuURAhR!hcGrw%q~C#2b_g<<6aJsAzMdO6rohJyP!TF$mm88+1QRQc49H6@mQbs-h8Lc2>FWcd-XQVwF8O>hLso_DIOy0Fh~tH<PeaT9rYRHh6~lj(hoP~)Ms>(!};sx?osiMjouuL^kFONtaB9hOic0|Q1R;4zRin9-qf3vxVTiK&1n_a=7C_jc;K?IJlE!JJM>@@;HU+m!%QnvB)r%b}{HlBZ4q#gH_XUZ^7Mra5^qOq|#CfU4C2L=_w+5#>}S3#}w4-B6o%wD5OZf$fx8`$QIiE)Ru8RiZ!kz%YVoy-x1+)7~FAk{o7}GAJ#tROV8UvIKsy&lqVa$~F=Udsf8yfnq)30Wn*ol?xN-u!(h>D>%?@$(9qvN=F2;d1qts>?>lf3?A=7(|I&uoHZZ@tuu&7J0UutW9u$$UMC~bgPXOy71$6_63I(F)Dy;d5m0DjuO1V!NEvz#z1aJ?=Q=Qx{Q;h?_Sh)#VYEafTTn!p`HQG`Lh(UQQo+yu2(AHO^RoIFu3b*#XxzDF>Xo><eM?2*DZ8u~oO0?oGsYM+iYi(Uc^x_y@UR3&%JhJbO`2MJi=BvYSd+8nQE1d0dZNja%tCh(%T<N3l3WmrUdm^cCvl{L4k4$@BTP^+RPR3vmUm9C$f>YE@2oIxpbexdqfY||Rtc||CQ%b?cD5<>6%Q>LL28FDr_t+T``|lJ%2*QxXBE!6G|hhj|6oP%yEiNJ0k99=LbE>H-+h)_<)|yTxz9d%0Wg<0S2CgDntH;cbeO1H8MvV*XJ^o_4Zzb<^>oQSj9y#5%1r6~Bxjx}W_jXhX)1tf87gvZG4iNKu##;F-;1FWPWh)^bKG~6Q_TrmP_A_4y)=9*mqw}f8Ln|sbkz4W$ZNqZ3ofkz)wZ!$a_@zv2r|$tD<Jn;(6`odAQKRJD>$Ioh=OGpA7G()%ger#r(w{_M}d5rqea8wbf&bMC`D-Dr|pP{5MFge+86tU2%OS5@!5Z&zV2t3_w~38^bagoYApp>g!OQIr|A$VA4pR#kQn9TKOX-d6?ys~')).decode("utf-8"))
_HIGH_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>bODa{Mnm_hFhJP0}}x)awyeGZH9i8|wiv7{F^7FxH2$Z^r(2%M{uD-mA#Sh^%UoGv=+;YQ9(Bl^Gcs`Sbsr{M)a;{rzvho&3|!C*Oa0_x|lKA8$T={&KrLxm%t5`>+4`umAP+f4+YF`>((K$KU?@>*t?Oet38PzuJfIzx?%=o1fnOc=P^bb@JxJ?qqe^eEsQ%?e^p3KR#`@Z@+%M`(b<Y`DAsu`1;4~`wu^ztk(OVf4u$h_RE{khrig|-Th-V?bye6Z~pw{<Ka!~N#A}x*=;|4zHjSKA8tSYaQ|ul)#Af^AU<v1zdyY7Z28v5$4y=Z8Zv$D;nQ*|Py-gP3uh1ZaNm;qIa$y8`tU3Au8;3;-fW}sME!aE1Ms#*yUAN0{$x6yO*`(t`{}S4W_^8_so-bn2ybte?>{V$o6p<Z<sw>sH(xz)>7FhZ(WehzmW!xeoPYYioiY1n(K|Mk?cmG@cri+c{=K<*SelPN`nEGCUAN})FkJ0RA4g&Ot8}`+{zH=kc0#j)$y*-A9*o&!IGP!2f1}UX!?@F-n>}~A^A1DUPE)Wh*TUfjHbZ!{^0Q^u1#M)}p_5PEV@vh1l)uU65e(tO2?ORRn>T$B_wU$$_<Ht!LLa<=JB)kJgCBlLCw=Vm>4XpIz~kRe-Zb>N>4#@{?BZ5A3#`fHFf}faF;88dt<Ls+@)j)Z5%SZ<j2P2`Hy_@=-@f_$%b&KlpWnTI_b>A^VbI`}Ut%ng@;i<+2amV*q&?vt+B+hP9|u?Y#hqaRzUcLD%<r;~=XLKkwf{P85@6mn=HtW&2Mf32X8>aa?g`whhox<q$-EEK-e!GF2M{>+hC#|)75FK8AR7zxDSaUG2t@m_!yk>CTy&t~L6vM@Wdl*)JfDB!>GZk23h<OZ4tmRm^8k$d!y{W`FyH(wa6)X$ynWW=Qd5=SW>0KbzdmjJ)8u;}*ih#x$Xz!KsIAcU4&mwR1wQ`u_`CgpARFmiWOpuToH7R$(_-I_$yv6=UcYy>$o(5Q0M@`GU_QbPikA$%u!jsY!dWRQ*fW^icw+dc{#I)Cpgw|;?OM0YLTLYQ%y5EDcmOE<S25@<8N$MhS@+1ZA#<-UdVSIBi~guD(ow|`_Ge6ofV_$n2fVORt$-)dzPo`Hn2)W2UPV{l0J-|2!kOh+L8d&Y&}l!RI`pCo%(w~0=7*cxzeF7yXWJMMjz}#)L$&Wqafqg4(Zl;_2d51T?-?Fl=oTOJeaF7N)f;qVEba$oI#M}C1wgOavOBEN$3Z!Sq2)n8JP}<!)As?_NRRqI5@+ZQS8=|;Ahi!}xodyeDEI4QpNv6p;aE-=_j`Uu&%DBH)U{(;Js2^cKHuK#zTe*7{uNj<CD@PgO0VeKAvgAPIP}LF7&KyicLW^p3Bf+=?ljEECBRp`OJl^O3e_FU#F|<sQ!LKI+c;R%wLbPA_E&oTI1Pt<ypboH7Bi9u#-F>qljR5$S3%To>+5gLtXhQV)3=6J;@<5oM_7mgf!=wXVE8$Y>*GkiMjM|icDb=Fpbop{?5=QpQiMUW5s0CJj#tH*roMUx##F8qhE_~2!QF=s@9%S!plS8+pAQrC^?ZDLQnvLD{ygrj@wIexYUUv0tqdX(Er&X~6=Z{VJ}dTG-cN)G%E7q)r9jC7>0_e}h0+u;KO~O(RqksEhU((%>Ap)JWvz|wrbwBD-Zr1gc;_}sTJf3)VAEyb*=r&~87D-xdA3LQE-*UZPB%LGmZwE!8?a$UpY%Zir%nqXFY}pdG(6ywEX><uSy3A^g?U|y*a7ovjbnD_xm5;JjBQg*<hW^0upIgV>=GR;LFv{YJve9sxSH8jrz07PubmB0@O6932S4O+gL;;*$%ZM`c|N^oJxF&tO`)XZx)g3;;MqRvWFUcH{%?{Lc*gYK2c}30dP0cnu`JjQqTD}S0DvVO+ba<ML8o!N7|4{^2F6Ukfr)?728O{@#BD5skzu$P_mtT;6=MTf2Th2!ktnc6yzP8w>8!;6%SW6-;l$+X8}W8=ld&W(XW82T_3ch_%5Bj0|E%+l4J+*$`;(%hl!Ckja%cZv%e`SaLX2tKm+&L!?AJh8U|{Q{;o2(!Nkns0`l*8J@37y|puvwu#E<XZ|9S3HL5~ZW3Ginu9=?Cqk$tbT9822YugI*^O+lBW7kFWiRRpZT$h&B+ZH3~=0jWAZp=0wES5tp_dN8vs0M<wFzHG6y=IYF^Cut$dRuUK*Hw}Oc6rhmDA$zxq5}53xQpUBqcr>@Ngn(<5j@Gk3SoF;3!3@GaXtMPsfW=MXTwI$i_KM7m!W$Ck0PYa;f-vvXG?a+1&<-SOJ@K7kpsa@-s=&{yBv{j^L3nctsHI?P0&A8GE!qZPGj*H6C}_cR*+3JgE3f4lR}5v)RY?G>6;W)yY5%;ES8z}fjNctnm9z7ZwG7$0>k92h^2b;g4o{MjXM{%XXWeUv<k92;eob@091n4#irlE4Y_AuUdiL6wV>PBbXgH@xUr^2Cvcv>a7(NJIU};A3J55|{pfE;jpXuH-A@O=K&Ya^t#G@wBKZ_OA_(EqAEP!ndL-wK~)-^bb6CmRIRe~Za$aAh>Gr1&)`X&KZ_{KFm$14z7*cA|jf8qp`87J=CNa$^Pn7Ct!m<SE96<TiP2{`x|O^ImP8l6r$cf|SV692O8P336X#c(B90C9?L5KfOMbA4PY5)xy<NEU*nJ?n#Q5^lyMSR)3`HIGXtW)WYNuR6r*h;2QzmJ4kIS-+2OAkLN)2wQez435qmKH`s!wWCS1YNIx!Rmf~U&d~5?)eoLyyGAwTsF%>Hf;Qw6v<g_PFQHkl3v0mc)UkqN`uW{K_G7s7mFTz_gw~_u#F3xD?Y=9odGNB8d{xR}34#X}k+|aPRw!h8SX_6{qb><*mtKZH3xrF~9}X*)MF^-QW%e!!kBWWq+N^`PXEu4MG!)GW?VM>kT+^3`VfRj1Z|)+J3=bUH2A~8=w*&C+dTrbR_?2zD;qQ>}D6gspntN&72pY9PBAJ3Mn2+q`olZbyqe=Z{k^>m!RO8lOp-6|`0rYmfiy7&bz*eOmY+`og`p%#Mprr(ws^MJ{6r1-<hhV65U9wU3%(!W#&RF}+>&xt+N&i67?xbcRX(Q+z{{wREBXZ=tFQ?~|zRWrvSMgb280qF|>(pc|nlp^M@ZFuBLd3~L6jFtJEihqZ$)T0SyV9ZZ$tIvmy6qADLc<)DNKI`@T@aCni9#CCG|?iQ<Y**Sp#iik1Swmu0HBmKQNS%S%8*NNK${~W<exU`B_r7Rr)O1kghM7T1u2OtKU+@m(J2rI^q!`hgB|NR{Q31%<XQtKPry$kKR-*to{m&SU#Rt`s~}2|%MpCt+Dg-&>RG<ZvQtx47}+-MhK$@@TWKv6USQb;)KoB}^}NuSyxgeIN$A58)5DYIY1RvKsc1u}lU<|hGJ&p^;KNcTD9Ig&X$)B+0Cz;XER=L|<OL#417nd<r-LmVPUz@dIH1LBrN<n8O@0#&_Vzf7s@=nfeoTFK^eVZEP}p{~x2nsEaI=!c5T$ua@h9k-2N9>0)F*`wldpG9gzH^U)g6SP9xcg;)y1kVGUJp=_XBG&&oqm%VtdR9*N@|&f@EC+TnxYH?A6Nhr|b?o>jt(<PFGVZ@cJ|3R|R6_Ch)*Zc*@hRBM%Vj{9vsS8w5H4K9X4803c{2*5jf=$A^6Y{sYy6i7?)D2Clm0SocS>p6pVmoiKzqZ#+zIX%FZ&GbDvYl3=c;i)`PD?V>nL#!#Fl3_a9*?5vggxHAxxV-6K|l@cDI241Twm|&o4?DpcWLY1$jIU%AydXOVDz~mWNqL!*EVCWT+oDG1raG*g};cVmNH5EUe!lPtt5w41m<f$_`L`VvabUS>MAW#XZNQpstF3&i+AQ+?x+@W5U&Nwm07jp&iw|s{zk&dC5921~O9QLSE9~Ltb_s4~Sl88beTzCd_T)k1$*fm=wd_(KfhnfgxT+~EZMhs2l-fOn%WA2*2UgD}rXnAS`4S+w(4!J^|6zg&chn3tVb_@rNE-!Wp-<#k}allu-^^!H3l>TdfkqpKa*6S(N?>=c8kQ*<bO=4pN;P7Nb6J~#N=mBI5J2D48$E5Wc`c)`epRK`9h&R`(O%D@~GDQwbbue>AJSeKaT$C~s74V`H(_%CdNwS6Qg=)%9yGm5K3u>MeDjU)KJqC&BBpc4X=_CiGDTeB}wwGkFCYr^9Zr3XtV0MA~_Q(0%AO~9&ZFxjC7DVf;wktLijLSvQ(oB*);{*>YKb<DYau9=>oJMgo)+kiofuTLfHcq9xDv+WGtf-s4G;o@~Ea6WohiW^faD;e!&{a2T$izUn;)P3D3$<!ZVv}gw#LCr0q7kcdhdgoAE(uaF2GkYGRlf^hrWQ@6uy>7v;1g0rTtTl2qNruQefQ5DL;|BNHFy8I@#-T0;QWt987O#V0WhB>?{_*%PD~MIhmI{R+?vs*L`HXi3IRviEz!j-^k8^l&Wo8kaX7NyA$BY6X0=IRgrv_c4$FHy{4>k=80y^Unz^>nMy)m=DimU6@YHr3wO;2_Q>%}yC`o9`G*OG_QiV|UUMo`!-g{tPWdq!&D<gU-f-*`?Y8CMMMJK)DB*}cM1VuLJfzprze@Ak@i{-I7*2(g4a%@raRbaH9x%ibA)0`2SQGj=!3ZW_Pk5;Tki9`=zO)42Bi6_22j(-z*GZ)zJdFlQQvZG!^fD%EEVhpb%0iFdX)tqFof2hIclA+ZIr1Ck@8yum0uTY|OOj*~M6A0`)C%h<;CatBk!@9pDj-Ad?$@AcuEIDA_wPB&j0ZDBuNm))2D{9YX{jR1*flh;G5$L{|vkE?H#U1Iaq+8F|0^1m>{A~`1CGo)oF<a9@UuA+G;o-4uG6?lHR0qTsQCy!nTwOVHMXf_Y>nf-S%Bho3Pg7>yk!Kl2g?5uQZ>4K_b>xX$W8Q}gXVFjFh}=ri;pVv`CH28VI+spb<H^|)ExAv;^VGQ?p!*x}r?*~Ccj0&fy*YP_11AWE#GR!<%R$q$5!k>yT!c3mWj+m&;zhl=5*8i1co`ak#Yw}TGyZ+wlwAq9iU{!V<4s$LEQ8MI6XdEZ`g|ILLflLOC^@o!O48D>Z2qSB65<5)b#e^aHG6ja(tDq3J=MFNYCEEv_NogULv!<D==+92&Gi;j(58~|P14zb!|nx(>zV;o=76$m6P176#wMlEJE;TR!TGVH-Gi4_hO=w=Qs_w&(|4j+OiEFA4zfZXaO-ypIZzmqy6yv++NdTC(~aWc?r&YPz-JBNM+Wjd^v05+os2|~y%K4iZ$dzB{tTw{ym7s!7CF&aAC-K2wz+{h2xFm(^?|tx`MPQCctGO^r%Mh4x0dd=0W~WdHogRy7N%|zo{Sz9NC$<}$c-REZ%39<f&q&#a>a{np>R?X!lP%gKtHf#`P=!6OiWl_l}NdYRX~IpgX5*>?nMW+2G@41v1L<|#0+l9xBbG?LMA=9npel>#d{!y7_}3Ch-%S;O<WLU)l?H-5gN!8Sa{`oM6L~t*0H<lIoKYI=P8)-F#Y_jO4Rd`&v!D{13+xdA@1~TQP8uDD$E8OU}i7J4+iF#A_g^~M}!5omZmT~<o3^SY8a@+QVo08N!IR49A!lT;MtS0FSMe8o!&W6*#aJys`%JP{MV?XMA@zt;ZrK9rT##@#N4S<*^jY568k(6TlOhS7A>P)=3#xi&9YZ>TUiffYZ?T(rBxAIW1JaPpHLOpXL4mVI2tUPQn6zi%#Q8z-0t2ux@&a%2p9T%{bf3Bg+hgwMkNO>3dW9GMyp}93kOv!lqxyI1yzIZ`0-|D;$8RYj=J=#v<_{x*}y?2wI%>olEEw@_eqWLYXFNzQXtgH#HrKLNTVIR>cwGHcATFWBqrR+fqS*H6rd((5|Po^pHBAx$C;~E3V$>?-pzWzhepf?=vo{gDlOylZnmBzvb+R>`92?3+4E8$WkkvizYB$iXVh3sax(KGO2@;oJSfGeo><E;wiB6(j0i`qf?ZjIR4dxGBT!^^DnOwZSJid-a;etGgQb!QMIAOBhT%?L&Lsj}ysG6mQB8uFrqx%%b%e%$M_H2CW#a_?t*LH)UP^1C0u<=B&z4<f7mg5QB>7IfLrDUA%-T41iW7KqE~LUUY|AZ|(wu1V!=9zYONnSY^DN6L@r+~1j7<E|cXF=oN{SzC3+GEkC>w!8=pyS+1YQW3M6Ewnc9FQ=ZvJacI$vE<aCvd(ilt?g^RYGQPU`0~YKi1f2U<inWkaotA=QyWU4E1jJhZs|Mk#`vcja7kbJ+@%G%UTz(}qVjlh5MFz<17tFP;u;=`m2I@J$KJx)2FGO!AaT9Wf(Q%e5+80Rdoh;Y1pxqOoFdk#n*}W30Tm3K0UI;CULWafIyo4E&n3Kmn6oyzLuec6u7XZL{R4d4K^n@fCIJu56+)4W2+aD08R_N;P@WlZ)e&HNo770X^KMG~CjqTF@G@)I_+6`<(e#)ml38N_3Lo%n~UrVy3F{ktjDlwgXp4(uvIzG0h4Si6Ig-)~cT3z~ZVU%1I_ishtwyiYtp^6ZVu%!1Y~0thOW&WtC^pmipSDFDXK}jOa2ABXWWOz2NASGz9%=pjb&#RMc;6b!?|t2`kKpC+f7)2YhvNlurwVtIiV)=XVMMs~lMc#}KO|MlPQsD!k+2*Pcq1^6IgmWJ2X7BGDq|sbiQMVd*gJPtAGYw_9F_n=P0t<K(3lI=vNOip0bd-Gs|f(#c7-d-JBK@P|K_4BFGU`Vu<CkTV86Ougf1lB;!&)uMo!$N{~f<iZLnGwZC9KtN6uUI|2DFAB3rjHHcm_lg?kE&eW2DAkMivd*Kkfv_3s^<9H*%~;KCfuJc3Qiqdt*!=~T4LTktO=6-Ye)7|j(qK0*{v@i(9IyTmU^OW&H52G73Hq>e?7R;lbJFENCYxUBNAO!OkFoX)r6&MA44<yEzSJUZk^1o@S&;+F+^%}?6SEf6{9lAarR12D&JG2PBjyc;-x$43Bojs8p#r-_l!l1D<(w6q)gv4X7o9b}kQJ;7-X;~O22}r~Wy5V{HANj|xgTnUqe$kjU8p-+W@#ZhDaWjb@}6gx4yuKfawm=YT#RoQEZ#~Er8-2slA4xqSPn4&a;mW&I3=C)J}ZHqc7^!)&I!z$3u9aMCZo|4#$6Wd*XU`$aVV;rsW1wGM)M-!d|<0wK+-0uaiGJ79G9oD#|2v1&eGDf?eg5Gxo7C6iYJzyP_3PN5F_!M4bRA&$ke>*UJa~s#)CS~P~0rhLDAF8o~^!F^aGh2cAQ+lENVGiXj^m^N&0nH+Mg~GqBs(r(nb<AVdeq)noY_wHW-X531Zb@G?U~(V#*mRH@Tj$$Nh~a*UKo(#csD<ldDE^E=V*7aYd?8M~0ron=)`qDZ8ns)W!Aiq(rN<B(~yIM=#bL73Q^)(#UxNQ!*8krb!QHb0%XBS0zJ@tWsU28ZA>AO%T(A<oR9KWVopAq@>dhl=+XmKeH%}!y^w0*#aWWxBW(e8`keI&K)Wz<a2)ETu^q-5LA(#?E8yo-&c!dO`dAs!%5W^j%OtS*H9|lsFW+u>35C-E1OfsfDwzL8xwg}o3{Ltq-mTyT|MFMiI(AI-!)5>w<x(MAsi;~0IYUVJdp=TXyw+dGT{pCyR)cgQNeE~8Fl#t#vz=e&YfQBK|@v5J?L}Oq&e$CF;81%v-Kt+rg8WA^#4JMW_Ti=RXoRK3(vzZ;V#nuoZD_LcB<4fkW_ACj#aF0RjX?yNzrFY?+|d+^1Y0ZCGa!~nW7!+E{^Eb0^neZb&P=`^M%aWo@K+y4w+n-o{wWB{1)Y2SdBFbKg!9p0!``6@#oXz+*X!{h`_@>8Z{3Y-D4{rhqP{8J<LH^AqI2=nj{jcwW?h?El*Oy$w!Hzb`dj3Oo+>a&*#qeL}J0s$&;u~MHK*<eQR}q`3i`gDe`U7NJ0$cq|qKlJeuf#TlJ38rKR#)^Qn>3dBKz=I=x&l4x>tW?Mc5{NioMUTlN&(mZXU6IUAIFluV^WF~vB(Kp78ayEcner(G-*nSwDH#CDv;N};lNH&JZ|iXFA9`7xnxF!BkuVWNO2Z!4O_>7}GD%DRl)hibxzR6HU&Ou1b8(Gjx*>dIzR`GY~2V0W>AsHWxFWdoi4Zp&PvxZS#|Gsl%Ja}>>w!U>cmuni$ts8x1#9IZ0F5T=J=z&@;xQ8BZ>oTW57y=2ImK$))6WEF6r9+gC~7h<?oJ+tHx*h%!@68q$OR2n8tV3rv-L7Jmqry_9=9Z6nGM$Mw1FuDy4nBKE8meS*z%5pNtp32(R7F?QBO0IGsnNIHEA%V1TJFVvxaW<apm*WSME^i9uB|{yIH~?8tYRlGc;0W(E!I}A*q*@IXGDF-=B}pmqRE#vY>wy|_R5CJi*2PS>_z0|WgO&It=jr62pe-}M>0=*?Vk)7imTKWcgG|D8YXUb?9VUtft<u!I0D-BYgZk#mQj}PDCh=6vTwO{P!E<+6=V4i?nAy~_lTz8hWg$2T%z!y!YOMrueueDqK6-Z|iAGA7YWc=A36<rg+5ptG#hyGXvL~flAM&I=S}^U_e`@}um~v02Q{(QdtM)0S;X(ztM80<h*<G@fwqxRwrwDB{zdRNv@7hs{7{e=M^t=tFu%q60@vC6QE#%*2Cq>F4fwz&uy)&Ua5jm<*8p?R84DQ&>w~AqP-i5{&Ypdc}7|m(8=mPM;1{sVfbFj72<I7T#Ogjh?vSCz`8VoslCIVHLr%IjylG9ipV<1JQSM1lHsHNfhT{|y<1!V03dpitl6BBmSmO3*aQkv<5PIF2!%^9Fk+Q^u!{)9F}b7iwdId~4|QP8fmLTH&tdf0R_bJA#QB6wca%(_?D4T`f2c*%#05^u^l5Hkrwgaev$4K5<b<pOgo#&LCso+#(+=sP*hF)e9p(U5}(gRlt}p#C#!fJr`FPLWj#eRxe3&V!DT<ypNEzuOW#q|CD{Gc%`^(SkDfTZFe(L-)wKmMR~xrP4&{a<3yqAHVka_QRs3iyFADR9$|+rqKdpAM%Wsm~cv{i8UhrvdZYg$gbAMLe@Z5>nx}8wVG%zEe|YXm6rGPRYa3$v7pWQ@(P6Jqy1uwgknckb6LM(<`*Srm8>fr!YjJzzGU6hSiTGnvbq!&Tfg8+ON)|dbyQgxq@!eEm8ho~7bNqE>+laLEGbj%ELNznU)_N35!rTIXPUBcD9+iY!lP65j^UOPE2NIe;86&3X@h`n9t+d@l1y!QR4u|L#Nxf8q1>WpPJumvour^dTZtWqJySKQTvpyubZDglh@9tStEi5m)bVu`*QsRc43XCCaHLgp+O#UFv^)k*X$+JLG3cQp>DP6Lky=-jlOj>H>YBgad3aTU%Y+P5HC)g@H*yf92R#RqhY&TT=bULsmuK|6W~pCQWxQ7s<V>WiD8&$%HzbqZ3oqACsx#c{bE5()s{t(8r&NKYq*^$WavOST#bQLVXS5>{%KO9#k-mP-J;KS8`!1>~Z!hv#Upl(jSB$ks2T!2N#Y%RCKZ&DWHE(vTP##yr<4kiQ{3YDyJw!c~YeaK)hA7;ybvE;-DT$B!2RZI6hP}^Qq0K&*f>&S5boHumXMsAU^ph;nc85?IK6G)3YHu-}y3R(?<;xgIt*cV)MuSLKCE^>)(P(i#J<6ljsIALdv#J@zO{EL{<xsUJ!EZP}OfFK_?bLti6mvT@j1MXd#%n`H<y8~y@rplFRE+`~1qD24Nl{;rpePoxHV%2P=#n~~nE;(zh~>OCBeZRSuv4ZbtjhHkE2t|`!VWn+DQKgo{<?TL$91+An5@Zn`6kiDP+B9c3(A5ObnSK!JkLx4d7;~o)Y}L$@S<|0B-?J=Um|r~+ExwcEY)OI*pWhxXRq8HZwJ7<)Y>PHvubeSPCIF4Jhhse4{dfW<C@Pe0&kBkL)8hS3qU2Y-Ux$!*_O#Emm9I|BY1y_xwZM7%lEZXg-wSoY!4jdS1+;NZvoqiqA|42W{@dkR9Y3SF9|J88fcaMwX3>aN#`ZQX)1$h^2~BBrxcg2R}}WeV%!WjA=7u~(em69tzqED!lSiP!Un3j6BVJ#jM`;~RvkKC?LMJyM$RdYq*E>7u44IW=Jf9PnJbhEaq>`gvYIip#e8U;{HR6Q+Yl0C*WKHpy$#f13C34xsf0P5tFz@=iZ~@DW+u$I0u(G`JgKFiBxZnEyarb2g@_4-V!v2HGw_iR(%;0Omuk>#N;Q|ML&YTJB8YNYEI#125#KY%Vfsq$LL)EXk8)R;f7)qy;IxO=eOc0)GA0uwZ&3?|iCQO{SZg3)kxDvt1mxXWx{Q}~NFwtQRDnCGU~b{aJ~h@8xKup-wnPitBVc<g3g64iW1FG;Xa`8_o1Ee`8ZDZglIOevYD{JL202ZC`-nRNcHUJ5WdcOp(IC@vq?%@FfIIB~g$)sP$z)?siIURdhw!$w3dGejFH=`YRn_k;>7dc#al}2U!da`sz_p}+e?TMCl}e*DA7H1l#%t00{66M<L??Zj3bw)<tN=+!vVbd1Z`4~*Zdq5cw0o)}WE>ngUpIN9TEoU`6MmOEdz#`tGcML<;WD~OC5;lMrCDj6tcuT4PfI~NuXU>CeL^1b#62zbCpjFI0ELz&krs2FKp{7uKIN$;vPXFTG;ah+ZPb0^GVd+_cK@hK6Wd8%JZ=SBy&M-f+&vA$5_HYG^tX>{*sj#7qmP#~k<!%eKP-qA&oP;W4_3pL*f&LJS}%7KME%dG3LkQD8;YLmJtk)%Q}HqV*NVEX6ackKu&2;!8p9{iw)E{t<W#D7!a@y-L9d0G5+4E_M!6RTx{OQOJU)`!F3S^$`G4eSW9KR?2GO+6U1Q2cgOI@ZloEJRN_XMF>#t>_OrGc-$<`19TW-i(5v{bDyRom_z4r1C)62KFA3pZ<GW?NOP`N=sAD#w-s}F6agA=+=X$0UD7(8j?$n1b?VvD~a)5L}Y^jR8@oFdo0wH^BXH{`z--*`)7p24P0$Z-4n?jLvm3-43V%>')).decode("utf-8"))
_ACTIONS = _LOW_ACTIONS
_FR_ITEMS = (
    "MELON",
    "MILK",
    "STRAWBERRY",
    "WOOL",
    "FERTILIZER",
    "WHEAT",
)
_FR_STATE = {
    0: {"last_step": -1, "due_step": -1, "due": {}},
    1: {"last_step": -1, "due_step": -1, "due": {}},
}
_WEED_STATE = {0: {}, 1: {}}
_WEED_REPLAY_STEPS = 8
_SHOP_PRODUCTS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if seat < len(farms) else {}


def _align_hands(action, obs):
    action = _copy_action(action)
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    if len(hands) < expected:
        hands.extend([["PASS"] for _ in range(expected - len(hands))])
    action["hands"] = [list(order or ["PASS"]) for order in hands[:expected]]
    return action


def _clip_opening_seed_surplus(action, obs, step):
    """Do not buy more seeds than the remaining first-day route can plant."""
    if int(step) != 1:
        return action
    demand = {}
    day_end = min(len(_ACTIONS), 24)
    for future in range(int(step), day_end):
        trace = _ACTIONS[future] or {}
        unit_actions = [
            trace.get("farmer") or ["PASS"],
            *list(trace.get("hands") or []),
        ]
        for order in unit_actions:
            if len(order) >= 2 and order[0] == "PLANT":
                demand[order[1]] = demand.get(order[1], 0) + 1
    seeds = _get(_get(obs, "private", {}) or {}, "seeds", {}) or {}
    action = _copy_action(action)
    market = []
    for order in action.get("market") or []:
        if len(order) < 3 or order[0] != "BUY_SEED":
            market.append(order)
            continue
        item = order[1]
        required = max(
            0,
            int(demand.get(item, 0))
            - max(0, int(_get(seeds, item, 0) or 0)),
        )
        order[2] = min(max(0, int(order[2] or 0)), required)
        if order[2] > 0:
            market.append(order)
    action["market"] = market
    return action


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _trace_actor_action(step, actor):
    trace = _ACTIONS[min(max(int(step), 0), len(_ACTIONS) - 1)] or {}
    if actor == "farmer":
        return list(trace.get("farmer") or ["PASS"])
    hands = trace.get("hands", []) or []
    return list(hands[actor] if actor < len(hands) else ["PASS"])


def _weed_repair_action(obs, action, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    game = _WEED_STATE[seat]
    if step == 0 or step < int(game.get("last_step", -1)):
        game = {"last_step": step, "active": {}}
        _WEED_STATE[seat] = game
    game["last_step"] = step
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    active = game.setdefault("active", {})

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else int(actor) + 1
        if index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[index] = list(transaction["intended"])
        elif 2 <= age <= 1 + _WEED_REPLAY_STEPS:
            unit_actions[index] = _trace_actor_action(step - 1, actor)
        else:
            active.pop(actor, None)

    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        actor = "farmer" if index == 0 else index - 1
        if actor in active or not isinstance(intended, list) or not intended:
            continue
        if intended[0] not in ("BUILD_PASTURE", "PLANT"):
            continue
        tile = _tile_at(farm, position)
        if not isinstance(tile, dict) or tile.get("kind") != "WEED":
            continue
        active[actor] = {"start": step, "intended": list(intended)}
        unit_actions[index] = ["DIG"]

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _fr_state(obs, step):
    seat = _seat(obs)
    state = _FR_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "due_step": -1, "due": {}}
        _FR_STATE[seat] = state
    state["last_step"] = step
    if 0 <= int(state.get("due_step", -1)) < step:
        state["due_step"], state["due"] = -1, {}
    return state


def _town_demand_now(obs, item, step):
    demand = 1 if item != "FERTILIZER" and step % 24 == 0 else 0
    if step % 4 != 0:
        return demand
    town = _get(obs, "town", {}) or {}
    for shop in list(_get(town, "unlocked_shops", []) or []):
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            demand += 2 if len(products) == 1 else 1
    return demand


def _future_quantity(step, item):
    future = step + 1
    if not 0 <= future < len(_ACTIONS):
        return 0
    return sum(
        max(0, int(order[2]))
        for order in (_ACTIONS[future].get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _pickup_reserve(action, item):
    reserve = 0
    for order in [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]:
        if isinstance(order, (list, tuple)) and len(order) >= 2 and order[0] == "PICKUP" and order[1] == item:
            try:
                reserve += max(0, int(order[2])) if len(order) >= 3 else 1
            except (TypeError, ValueError):
                reserve += 1
    return reserve


def _existing_sell(action, item):
    return sum(
        max(0, int(order[2]))
        for order in (action.get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _repay(action, state, step):
    if int(state.get("due_step", -1)) != step:
        return action
    due = {str(item): max(0, int(quantity)) for item, quantity in dict(state.get("due", {})).items()}
    action = _copy_action(action)
    market = []
    for raw in action.get("market") or []:
        order = list(raw)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in due and due[order[1]] > 0:
            requested = max(0, int(order[2]))
            reduction = min(requested, due[order[1]])
            requested -= reduction
            due[order[1]] -= reduction
            if requested <= 0:
                continue
            order[2] = requested
        market.append(order)
    action["market"] = market[:10]
    state["due_step"], state["due"] = -1, {}
    return action


def _front_run(action, obs, state, step, prepaid=None):
    if not _FR_ITEMS:
        return action
    prepaid = prepaid or {}
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    moved = {}
    action = _copy_action(action)
    for item in _FR_ITEMS:
        target = max(
            0,
            _future_quantity(step, item)
            - max(0, int(prepaid.get(item, 0) or 0)),
        )
        if target <= 0 or _town_demand_now(obs, item, step) > 0:
            continue
        stock = max(0, int(_get(shed, item, 0) or 0))
        reserve = _pickup_reserve(action, item) + _existing_sell(action, item)
        quantity = min(target, max(0, stock - reserve))
        if quantity <= 0:
            continue
        market = [list(order) for order in (action.get("market") or [])]
        existing = next((order for order in market if len(order) >= 3 and order[0] == "SELL" and order[1] == item), None)
        if existing is not None:
            existing[2] = max(0, int(existing[2])) + quantity
        elif len(market) < 10:
            market.append(["SELL", item, quantity])
        else:
            continue
        action["market"] = market[:10]
        moved[item] = moved.get(item, 0) + quantity
    if moved:
        state["due_step"] = step + 1
        state["due"] = moved
    return action


_ENABLE_NINTH_COW = False
# V16-RC5-R5: bounded, public-state COW placement recovery.
_COW_ALIGN_STATE = {
    0: {"last_step": -1, "active": {}},
    1: {"last_step": -1, "active": {}},
}


def _empty_cow_pasture(tile):
    return (
        isinstance(tile, dict)
        and tile.get("kind") == "PASTURE"
        and not tile.get("animal")
    )


def _adjacent_cow_pasture_move(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
    except (IndexError, TypeError, ValueError):
        return None
    for operation, dx, dy in (
        ("EAST", 1, 0),
        ("WEST", -1, 0),
        ("SOUTH", 0, 1),
        ("NORTH", 0, -1),
    ):
        if _empty_cow_pasture(_tile_at(farm, (x + dx, y + dy))):
            return [operation]
    return None


def _cow_inventory(obs, actor_index):
    private = _get(obs, "private", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    if actor_index >= len(inventories):
        return 0
    return max(
        0,
        int(_get(inventories[actor_index] or {}, "COW", 0) or 0),
    )


def _is_cow_place(order):
    return (
        isinstance(order, (list, tuple))
        and len(order) >= 2
        and order[0] == "PLACE"
        and order[1] == "COW"
    )


def _cow_place_alignment(obs, action, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    state = _COW_ALIGN_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "active": {}}
        _COW_ALIGN_STATE[seat] = state
    state["last_step"] = step
    active = state.setdefault("active", {})
    if step % 24 == 0:
        active.clear()

    farm = _farm(obs, seat)
    positions = [
        _get(farm, "farmer"),
        *list(_get(farm, "hands", []) or []),
    ]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]

    for actor, transaction in list(active.items()):
        actor_index = 0 if actor == "farmer" else int(actor) + 1
        if actor_index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[actor_index] = ["PLACE", "COW", 1]
        elif age >= 2:
            unit_actions[actor_index] = _trace_actor_action(step - 1, actor)

    if 0 <= step <= 280:
        for actor_index, (position, intended) in enumerate(
            zip(positions, unit_actions)
        ):
            actor = "farmer" if actor_index == 0 else actor_index - 1
            if actor in active or not _is_cow_place(intended):
                continue
            if _cow_inventory(obs, actor_index) <= 0:
                continue
            if _empty_cow_pasture(_tile_at(farm, position)):
                continue
            movement = _adjacent_cow_pasture_move(farm, position)
            if movement is None:
                continue
            active[actor] = {"start": step}
            unit_actions[actor_index] = movement

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _owned_cows(obs):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    total = 0
    for row in list(_get(farm, "tiles", []) or []):
        for tile in list(row or []):
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and tile.get("animal") == "COW"
            ):
                total += 1
    private = _get(obs, "private", {}) or {}
    total += max(0, int(_get(_get(private, "shed", {}) or {}, "COW", 0) or 0))
    for inventory in list(_get(private, "inventories", []) or []):
        total += max(0, int(_get(inventory or {}, "COW", 0) or 0))
    return total


def _cow_target_after_buy(step):
    """Return the selected route's cumulative cow target at a buy step."""
    step = int(step)
    current = _ACTIONS[step] if 0 <= step < len(_ACTIONS) else {}
    if not any(
        len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]
        for order in (current.get("market") or [])
    ):
        return None
    return sum(
        max(0, int(order[2] or 0))
        for action in _ACTIONS[: step + 1]
        for order in (action.get("market") or [])
        if len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]
    )


def _reconcile_scheduled_cows(obs, action, step):
    """Increase an existing cow order after an earlier partial purchase.

    BUY_ANIMAL executes per unit, so a two-cow order can silently buy only
    one when cash is a few dollars short.  Later route turns already contain
    the matching placement slots; enlarging a later scheduled order restores
    the selected route's observable herd target without adding a market slot
    or buying beyond its cumulative plan.
    """
    target = _cow_target_after_buy(step)
    if target is None:
        return action
    missing = max(0, target - _owned_cows(obs))
    if missing <= 0:
        return action
    action = _copy_action(action)
    for order in action.get("market") or []:
        if len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]:
            order[2] = max(max(0, int(order[2] or 0)), missing)
            break
    return action


def _guarded_demand_cow9(obs, action, step):
    if not _ENABLE_NINTH_COW or step != 289 or _owned_cows(obs) != 8:
        return action
    farms = list(_get(obs, "farms", []) or [])
    opponent_index = 1 - _seat(obs)
    opponent = farms[opponent_index] if opponent_index < len(farms) else {}
    opponent_cows = sum(
        1
        for row in list(_get(opponent, "tiles", []) or [])
        for tile in list(row or [])
        if isinstance(tile, dict) and tile.get("animal") == "COW"
    )
    if opponent_cows < 9:
        return action
    shops = list(
        _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    )
    milk_demand = sum(
        shop in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
        for shop in shops
    )
    farm = _farm(obs, _seat(obs))
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    milk_price = float(_get(prices, "MILK", 0) or 0)
    money = float(_get(farm, "money", 0) or 0)
    if (
        milk_demand < 3
        or not math.isfinite(milk_price)
        or not math.isfinite(money)
        or not milk_price >= 225
        or not money >= 800
    ):
        return action
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]
    if len(market) >= 10 or any(
        len(order) >= 2
        and order[0] == "BUY_ANIMAL"
        and order[1] == "COW"
        for order in market
    ):
        return action
    market.append(["BUY_ANIMAL", "COW", 1])
    action["market"] = market[:10]
    return action



# The second-order market counter uses the selected route's own premium-sale
# schedule.  Only public market and farm state can activate its H7 prepayment.
_LOW_META_SALES = {148: {'WOOL': 6}, 151: {'WOOL': 6}, 197: {'MILK': 12}, 222: {'WOOL': 4}, 223: {'WOOL': 4}, 256: {'MELON': 12}, 257: {'MELON': 12}, 258: {'MELON': 12}, 259: {'MELON': 12}, 262: {'MELON': 12}, 264: {'MELON': 12, 'MILK': 6}, 288: {'MILK': 6}, 312: {'MILK': 6}, 336: {'MILK': 9}, 357: {'WOOL': 14}, 360: {'MILK': 6}, 366: {'MILK': 12}, 378: {'WOOL': 6}, 380: {'STRAWBERRY': 6}, 384: {'MILK': 6, 'STRAWBERRY': 2}, 396: {'MELON': 6}, 408: {'MELON': 6, 'MILK': 6}, 415: {'WOOL': 17}, 420: {'MELON': 12}, 421: {'MELON': 5}, 422: {'MELON': 1}, 427: {'WOOL': 1}, 428: {'STRAWBERRY': 6}, 430: {'MELON': 6}, 431: {'MELON': 6}, 432: {'MILK': 24, 'STRAWBERRY': 8, 'MELON': 2}, 438: {'MELON': 2}, 439: {'MELON': 1}, 440: {'MELON': 1}, 453: {'STRAWBERRY': 5}, 454: {'WOOL': 4}, 456: {'MILK': 6, 'STRAWBERRY': 2}, 473: {'WOOL': 2}, 474: {'WOOL': 6}, 476: {'STRAWBERRY': 6}, 480: {'MILK': 25, 'STRAWBERRY': 8}, 481: {'MILK': 5}, 504: {'STRAWBERRY': 8}, 510: {'MILK': 6}, 516: {'WOOL': 5}, 517: {'WOOL': 1}, 519: {'STRAWBERRY': 6, 'WOOL': 2}, 525: {'STRAWBERRY': 14, 'MILK': 3}, 528: {'STRAWBERRY': 24, 'MILK': 2}, 545: {'MILK': 19}, 551: {'STRAWBERRY': 8}, 552: {'STRAWBERRY': 13, 'MILK': 6}, 561: {'WOOL': 1}, 564: {'WOOL': 11}, 567: {'STRAWBERRY': 6}, 571: {'STRAWBERRY': 8}, 575: {'STRAWBERRY': 6}, 576: {'STRAWBERRY': 18}, 579: {'WOOL': 4}, 582: {'MILK': 1}, 583: {'MILK': 17}, 585: {'MILK': 6}, 599: {'MILK': 6}, 600: {'STRAWBERRY': 20}, 606: {'WOOL': 5}, 607: {'STRAWBERRY': 2}, 611: {'MILK': 6}, 615: {'WOOL': 3, 'STRAWBERRY': 6}, 620: {'STRAWBERRY': 8}, 624: {'STRAWBERRY': 9, 'WOOL': 2}, 628: {'WOOL': 2}, 631: {'MILK': 10}, 634: {'MILK': 14}, 648: {'STRAWBERRY': 13, 'MILK': 6, 'WOOL': 4}, 663: {'STRAWBERRY': 6}, 668: {'WOOL': 4}, 669: {'STRAWBERRY': 8}, 672: {'MILK': 24, 'STRAWBERRY': 16, 'WOOL': 4}, 695: {'STRAWBERRY': 2}, 696: {'STRAWBERRY': 10, 'MILK': 6, 'WOOL': 4}, 713: {'MILK': 6}, 717: {'MILK': 15, 'WOOL': 4}, 718: {'MILK': 3}}
_HIGH_META_SALES = {148: {'WOOL': 6}, 151: {'WOOL': 6}, 193: {'MILK': 6}, 197: {'MILK': 6}, 222: {'WOOL': 4}, 223: {'WOOL': 4}, 256: {'MELON': 12}, 257: {'MELON': 24}, 259: {'MELON': 12}, 262: {'MELON': 12}, 264: {'MELON': 12, 'MILK': 6}, 288: {'MILK': 6}, 312: {'MILK': 6, 'WOOL': 8}, 336: {'MILK': 9, 'WOOL': 6}, 360: {'MILK': 6, 'WOOL': 6}, 367: {'WOOL': 6}, 384: {'MILK': 18, 'WOOL': 14, 'STRAWBERRY': 8}, 396: {'MELON': 6}, 408: {'MELON': 6, 'WOOL': 4, 'MILK': 6}, 414: {'WOOL': 12}, 420: {'MELON': 6}, 424: {'MELON': 12}, 430: {'MILK': 3}, 432: {'MELON': 17, 'STRAWBERRY': 8, 'MILK': 9, 'WOOL': 4}, 437: {'MELON': 1}, 455: {'MILK': 3}, 456: {'WOOL': 22, 'STRAWBERRY': 14, 'MILK': 3}, 468: {'WOOL': 4}, 475: {'STRAWBERRY': 6}, 480: {'STRAWBERRY': 10, 'MILK': 12, 'WOOL': 6}, 504: {'STRAWBERRY': 6, 'MILK': 3, 'WOOL': 12}, 509: {'MILK': 3}, 516: {'WOOL': 4}, 519: {'STRAWBERRY': 10}, 520: {'WOOL': 5}, 528: {'STRAWBERRY': 29, 'WOOL': 16, 'MILK': 12}, 552: {'MILK': 6, 'WOOL': 8}, 553: {'STRAWBERRY': 11}, 562: {'WOOL': 8}, 563: {'WOOL': 6}, 571: {'STRAWBERRY': 6}, 576: {'MILK': 12, 'WOOL': 4, 'STRAWBERRY': 17}, 590: {'STRAWBERRY': 1}, 591: {'STRAWBERRY': 15, 'WOOL': 8}, 600: {'WOOL': 16}, 605: {'MILK': 5}, 606: {'STRAWBERRY': 7}, 607: {'MILK': 1}, 612: {'WOOL': 4}, 619: {'STRAWBERRY': 1}, 622: {'STRAWBERRY': 2}, 623: {'WOOL': 4}, 624: {'MILK': 11}, 629: {'STRAWBERRY': 4, 'MILK': 1}, 634: {'STRAWBERRY': 10}, 642: {'STRAWBERRY': 13}, 648: {'WOOL': 16}, 649: {'MILK': 6, 'STRAWBERRY': 8}, 652: {'STRAWBERRY': 8}, 663: {'WOOL': 4}, 664: {'STRAWBERRY': 6, 'WOOL': 4}, 665: {'STRAWBERRY': 1}, 666: {'STRAWBERRY': 9}, 671: {'WOOL': 4}, 672: {'STRAWBERRY': 14, 'MILK': 12, 'WOOL': 12}, 696: {'MILK': 6, 'STRAWBERRY': 3, 'WOOL': 8}, 713: {'MILK': 6}, 714: {'STRAWBERRY': 2, 'WOOL': 8}, 717: {'MILK': 6, 'WOOL': 8}}
_META_SALES = _LOW_META_SALES
_META_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_META_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_META_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_META_HORIZON = 4
_META_H5_LEAD = 7


def _new_meta_state():
    return {
        "last_step": -1,
        "clone_confidence": 0,
        "h4_active": False,
        "h4_evidence": 0,
        "h5_due": {},
        "prev_market_inv": None,
        "prev_town_shops": (),
        "prev_action": None,
        "prev_shed": None,
        "prev_prices": None,
        "prev_step": -1,
    }


_META_STATE = {0: _new_meta_state(), 1: _new_meta_state()}


def _meta_state(obs, step):
    seat = _seat(obs)
    state = _META_STATE[seat]
    if step == 0 or step <= int(state.get("last_step", -1)):
        state = _new_meta_state()
        _META_STATE[seat] = state
    return state


def _meta_public_signature(farm):
    counts = {
        item: 0
        for item in (
            "COW", "SHEEP", "GOOSE", "WHEAT", "CARROT", "TOMATO",
            "STRAWBERRY", "MELON", "PASTURE", "COOP", "WEED",
        )
    }
    for row in _get(farm, "tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value in counts:
                    counts[value] += 1
                    break
    positions = [
        _get(farm, "farmer", [0, 0]),
        *list(_get(farm, "hands", []) or []),
    ]
    return (
        len(_get(farm, "hands", []) or []),
        tuple(sorted(_get(farm, "unlocked_quadrants", []) or [])),
        tuple(sorted(tuple(position) for position in positions)),
        tuple(counts[item] for item in sorted(counts)),
    )


def _meta_signature_distance(left, right):
    distance = abs(left[0] - right[0])
    distance += 3 * abs(len(left[1]) - len(right[1]))
    distance += sum(abs(a - b) for a, b in zip(left[3], right[3]))
    if left[2] != right[2]:
        distance += 2
    return distance


def _meta_update_clone_profile(obs, step, state):
    if step not in (4, 24) and not (step >= 48 and step % 24 == 0):
        return
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return
    player = _seat(obs)
    distance = _meta_signature_distance(
        _meta_public_signature(farms[player]),
        _meta_public_signature(farms[1 - player]),
    )
    confidence = int(state.get("clone_confidence", 0))
    if distance <= 1:
        confidence = min(8, confidence + 1)
    elif distance <= 4:
        confidence = max(0, confidence - 1)
    else:
        confidence = max(0, confidence - 3)
    state["clone_confidence"] = confidence


def _meta_sell_qty(action, item):
    return sum(
        max(0, int(order[2] or 0))
        for order in (action or {}).get("market", []) or []
        if (
            isinstance(order, list)
            and len(order) >= 3
            and order[0] == "SELL"
            and order[1] == item
        )
    )


def _meta_trace_sell_qty(step, item):
    return max(0, int((_META_SALES.get(step) or {}).get(item, 0) or 0))


def _meta_town_demand(step, shops, item):
    demand = 0
    if step % 4 == 0:
        for shop_name in shops or ():
            products = _SHOP_PRODUCTS.get(shop_name, ())
            if item in products:
                demand += 2 if len(products) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        demand += 1
    return demand


def _meta_remember_market(obs, step, action, state):
    market = _get(obs, "market", {}) or {}
    state["prev_market_inv"] = dict(_get(market, "inventory", {}) or {})
    state["prev_prices"] = dict(_get(market, "prices", {}) or {})
    town = _get(obs, "town", {}) or {}
    state["prev_town_shops"] = tuple(
        _get(town, "unlocked_shops", []) or []
    )
    state["prev_action"] = copy.deepcopy(action)
    private = _get(obs, "private", {}) or {}
    state["prev_shed"] = dict(_get(private, "shed", {}) or {})
    state["prev_step"] = step


def _meta_observe_h4(obs, step, state):
    prev_market = state.get("prev_market_inv")
    prev_action = state.get("prev_action")
    prev_shed = state.get("prev_shed")
    prev_step = int(state.get("prev_step", -1))
    if (
        state.get("h4_active")
        or prev_market is None
        or prev_action is None
        or prev_shed is None
        or prev_step != step - 1
        or int(state.get("clone_confidence", 0)) < 3
    ):
        return

    market = _get(obs, "market", {}) or {}
    current_inventory = _get(market, "inventory", {}) or {}
    current_prices = _get(market, "prices", {}) or {}
    previous_prices = state.get("prev_prices") or {}
    for item in _META_ITEMS:
        if float(previous_prices.get(item, 2) or 0) <= 1:
            continue
        if float(current_prices.get(item, 2) or 0) <= 1:
            continue
        target = prev_step + 4
        if _meta_trace_sell_qty(target, item) <= 0:
            continue
        if _meta_trace_sell_qty(prev_step, item) > 0:
            continue
        if any(
            _meta_trace_sell_qty(candidate, item) > 0
            for candidate in range(prev_step + 1, target)
        ):
            continue
        own_requested = _meta_sell_qty(prev_action, item)
        own_supply = min(
            max(0, int(prev_shed.get(item, 0) or 0)),
            own_requested,
        )
        if own_supply < 2:
            continue
        demand = _meta_town_demand(
            prev_step,
            state.get("prev_town_shops") or (),
            item,
        )
        observed_delta = int(current_inventory.get(item, 0) or 0) - int(
            prev_market.get(item, 0) or 0
        )
        opponent_supply = observed_delta + demand - own_supply
        if (
            opponent_supply >= 2
            and 0.40 <= opponent_supply / max(1, own_supply) <= 2.50
        ):
            state["h4_evidence"] = int(state.get("h4_evidence", 0)) + 1
            state["h4_active"] = True
            return


def _meta_h5_counter(action, obs, step, state):
    if not state.get("h4_active"):
        return False
    target = step + _META_H5_LEAD
    if target >= len(_ACTIONS):
        return False
    orders = [list(order) for order in action.get("market", []) or []]
    if len(orders) >= 10:
        return False
    already = {}
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(
                0, int(order[2] or 0)
            )
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    shops = tuple(
        _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    )
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    choices = []
    for item in _META_ITEMS:
        planned = _meta_trace_sell_qty(target, item)
        if planned <= 0 or _meta_town_demand(step, shops, item) > 0:
            continue
        available = max(
            0, int(_get(shed, item, 0) or 0) - already.get(item, 0)
        )
        quantity = min(available, planned)
        if quantity <= 0:
            continue
        price = float(_get(prices, item, _META_BASE_PRICE[item]) or 0)
        priority = price * quantity * _META_GLUT_WEIGHT[item]
        choices.append((priority, item, quantity))
    if not choices:
        return False
    _, item, quantity = max(choices)
    action["market"] = [["SELL", item, quantity], *orders][:10]
    due = state.setdefault("h5_due", {}).setdefault(target, {})
    due[item] = max(0, int(due.get(item, 0) or 0)) + quantity
    return True


def _meta_repay_h5(action, step, state):
    """Remove quantities prepaid by the H7 counter from their route sale."""
    due = dict(state.setdefault("h5_due", {}).pop(int(step), {}) or {})
    if not due:
        return
    market = []
    for raw in action.get("market", []) or []:
        order = list(raw)
        if (
            len(order) >= 3
            and order[0] == "SELL"
            and max(0, int(due.get(order[1], 0) or 0)) > 0
        ):
            reduction = min(max(0, int(order[2] or 0)), due[order[1]])
            order[2] = max(0, int(order[2] or 0)) - reduction
            due[order[1]] -= reduction
            if order[2] <= 0:
                continue
        market.append(order)
    action["market"] = market[:10]


def _meta_front_run(action, obs, step, state):
    _meta_repay_h5(action, step, state)
    if _meta_h5_counter(action, obs, step, state):
        return
    if int(state.get("clone_confidence", 0)) < 1 or _META_HORIZON <= 0:
        return
    orders = [list(order) for order in action.get("market", []) or []]
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(
                0, int(order[2] or 0)
            )
    planned = {}
    end = min(len(_ACTIONS), step + _META_HORIZON + 1)
    for future_step in range(step + 1, end):
        distance = future_step - step
        for item, quantity in (_META_SALES.get(future_step) or {}).items():
            if item not in planned:
                planned[item] = [distance, quantity]
            else:
                planned[item][1] += quantity
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    choices = []
    for item, (distance, quantity) in planned.items():
        available = max(
            0, int(_get(shed, item, 0) or 0) - already.get(item, 0)
        )
        quantity = min(available, quantity)
        if quantity <= 0:
            continue
        price = float(_get(prices, item, _META_BASE_PRICE[item]) or 0)
        priority = (
            price * quantity * _META_GLUT_WEIGHT[item]
            + (_META_HORIZON + 1 - distance) * _META_BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        action["market"] = [*orders, ["SELL", item, quantity]][:10]



_ROUTE_DECISION_STEP = 168
_ROUTE_STATE = {
    0: {"last_step": -1, "shops": (), "expert": None},
    1: {"last_step": -1, "shops": (), "expert": None},
}


def _select_route(obs, step):
    """Select the wool route only when early public shop demand supports it."""
    seat = _seat(obs)
    state = _ROUTE_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "shops": (), "expert": None}
        _ROUTE_STATE[seat] = state
    state["last_step"] = step
    if step <= _ROUTE_DECISION_STEP:
        town = _get(obs, "town", {}) or {}
        state["shops"] = tuple(
            str(value)
            for value in (_get(town, "unlocked_shops", []) or [])
        )
    if state.get("expert") is None and step >= _ROUTE_DECISION_STEP:
        shops = tuple(state.get("shops") or ())
        dominated = (
            len(shops) >= 2
            and shops[0] == "ICE_CREAM_SHOP"
            and shops[1] == "YARN_STORE"
        )
        state["expert"] = (
            "high" if "YARN_STORE" in shops and not dominated else "low"
        )
    if state.get("expert") == "high":
        return _HIGH_ACTIONS, _HIGH_META_SALES
    return _LOW_ACTIONS, _LOW_META_SALES


def agent(obs, config=None):
    """Return the V4 action for one Kaggriculture observation."""
    try:
        global _ACTIONS, _META_SALES
        raw_step = max(0, int(_get(obs, "step", 0) or 0))
        _ACTIONS, _META_SALES = _select_route(obs, raw_step)
        if len(list(_get(obs, "farms", []) or [])) < 2:
            return {"farmer": ["PASS"], "hands": [], "market": []}
        step = min(
            max(0, int(_get(obs, "step", 0) or 0)),
            len(_ACTIONS) - 1,
        )
        meta = _meta_state(obs, step)
        _meta_update_clone_profile(obs, step, meta)
        _meta_observe_h4(obs, step, meta)
        meta["last_step"] = step

        action = _clip_opening_seed_surplus(
            _copy_action(_ACTIONS[step]), obs, step
        )
        action = _weed_repair_action(
            obs,
            action,
            step,
        )
        action = _cow_place_alignment(obs, action, step)
        action = _reconcile_scheduled_cows(obs, action, step)
        action = _guarded_demand_cow9(obs, action, step)
        state = _fr_state(obs, step)
        action = _repay(action, state, step)
        action = _front_run(
            action,
            obs,
            state,
            step,
            prepaid=dict(
                (meta.get("h5_due", {}) or {}).get(step + 1, {}) or {}
            ),
        )
        action = _align_hands(action, obs)

        _meta_front_run(action, obs, step, meta)
        _meta_remember_market(obs, step, action, meta)
        return action
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [
                ["PASS"]
                for _ in (_get(farm, "hands", []) or [])
            ],
            "market": [],
        }
