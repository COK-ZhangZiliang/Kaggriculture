"""Kaggriculture V6: behavior-routed recovery-aware execution control.

The deterministic policy retains the V5 public-shop route selector and adds a
conservative step-72 observable-state gate for one recurrent public opponent
farm shape.  Matching episodes switch to a third public-replay consensus route;
all other episodes keep the V5 low/high routes and recovery controls.  See
THIRD_PARTY_NOTICES.md for provenance and modifications.
"""
import base64
import copy
import json
import math
import zlib
from collections import Counter


_LOW_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>Z1oa{Mnm^Pp~aH%Z?(Qm-W}XDCqAHr4}TFo4%EV5|>g-;Dk5){^~ERWC9!GV>M58R*t(wyNIu%Z!YS{Q3XR{^Qr*{{FY$&i>`+vmd^Gy8ZCW=bJANU+=ePkLPFq`RjlG`~Q6V%eRkz|Mj>3`rH40`~36S$4^gx)js_2^{>C&{PgL^o7=PVv-fwqv-4&1^_P#^?dQQCzHGN2zJ0y>xV?EeJHMQK{p0rb?x(Z!#qsB#@9#c*egAO!ADhR=f1D3H_W9HMKY#svdedUix1Y~;+b<7KZT;!){^8@(r{h<X595LOvc0`Mz4c=H*2CiluL2DjzV`HKIu)n^lh>KE2YYyI$<v%HMt$A?ioEOd?alkGHJ+$HhyMWHHfc9`>;AtC$Fph2(|13e7Q?8o`<XI+=8o|8X8Qiq^0;}}-cJ|N^t<uuflGHeT|{5*zD^fWyEy;!&z&*)X3{%0mF?h+2Y50{r~bXa*)Pq*kDhntpzEQzJPlX-(!(eWf8|aW*nenpz)omZFnP;<?7^4~hNGFW_BZ;B?Z=%C-RQZ~op&0-cAAWJxeyLFuo=vwm7gu6E@&f*4jq5;4lUKkQvSxDM=*r@69&wYH*fkN9^Y~N@a^pVf<D9s?lkU|2k(DLC%y0U>4bObz~TQ6-qiKE?uS=+?BrItFsw=EFb!NFeV#f!TO-@|#al47N61ebGonum-rwEcZr?xr@~7?n!>8L%|294oIt^a>C4nW9e#cC6aJaPx?J@Vz(Gi*a*tp8qj{yttO|SpJ{7(D0%6qr2{a3U}fO*%Lj{_qdEZmHr0gMs2CvdO!OFLvH^F9oF>-EtcK;YO13{vK*z)#)-*;t@Y?gN=eAli=wf7EVr(t)xERkD4R4Mcr&fBuQ5Q*(V4;K_X)^p*q812FDSk8F)WfAhD%39&8x_JtnjnyLghdtt-+`_uYAO}_Vm4Yg81?z~|@ZH2aX2v1*3@bPcQ-~AneY@~CM-MOG~${b`&i(@+mXW15e{jsY>?qA0N2n{>}<}KVHdCAZVyUQ>moRy-2mBHl36T?6Cw^FkQ^%0D0Y27jlq5WH*;RKuT1W?9b#h^E52op0Fx<_6Onfv~t?=SlPqCe`3bX2j2{b|!7Ag{v30oP$v%iu}0?`~iP=3{H1SJIUafLyhxuxEK@kf|6{7->JDI#kgGX51KK^YP~XFILC;*){<PN2C^@p*r>@IYh&;sPI18!D$1-M}|iU-Qt6O?AY^LV}p*2#p9q1N6N>j0O&PZcBeIZ7?e{OS|0S%6Vc@}d>?R)^r-)VI74r^jPnHsseN$EUHijExxYX5#TW$Zh~>0?+VdlN<`rh6E+VGY-iZ0~aDTJ=VS9i7S76DcU_Ztyy`pc2+}LGz=#MqfXvE@i1|0AO!M@Pl889QK0AKblwGopnR5zE2HMCBKSX>Nm<6u!~eH=d=uXO)$8V-55kq4U=Gm<;TpG)4!bOe&C!0LDC>*r=>Ekg9^xuKc3cYDhb7NS6)k33E={34I5aU{P-8(%ASxd~f91-s_rF>!oSgh8?qh@paxSH+p8zPbm-WUdv4Rtzq|-QC^oQ?3#;t@eN1PtdpX@xxi#);sz0xVM3?rK3|b2N`dr6Om{-)Yh#a8@%IL39sejM2MgqjO$+tlq`@w*4t1>O%d}$?6_a%zLsF95@%2MU22rIHoEH~WfFSZd`jb;TPtZL)<giCP6N-eCL)w^Kx7+ddz5!Up!4l?qoZ$nT4c5X8)o!L9~5xvv;gunpD9Pf13t;byq(L6+5}UW7paKdI5xKOEiafx95%;99-HRq%Hb`*AkhI4lu`{+fQ>eQ>z7?;I$ELl)7}6XU$-~8@k0(N80W=BWU^rzwVyK|vk;_vo2E%p0-XyfFo5hBSqh+iVE%8MG<U}4KL(#jnz=)It5^?g2T^{Xp5)IGi^D4r{)eIgY*PNuop@x63i`J!@gdlLYu8IJ+pG;aPgfTF;Ey!3Cyu=U27qa6gvPn;GJCGsznIBGL2lB)Ch!bWqcclec_kYS1mh;pIi&?)%oAr@WSkAy8VrBtkOc!8W30x8pXn?d9;vh>gI7}?ft-c^3JLmsklaPs2dT3Fud%lgQY{)13R{~1{w(BqBywuN?OHR~IwfEpudE>&Y?=PRs3Xptm8y}Eap4SAZpdP~QZ}*1ObUrzpvNgcn7}`Ny8ZKhEn1#a`%6C|GwjHrIoj{`=NB(TR6zpWhoPKRbkf0k3?mL4*RA-2;AO|P2~Gn+j3|_D8;np1sls#0hk?`lWWf*Z<OV}&4SkN9nA4o|Zia`8&qvi0&GfOn@Uhg^qeGHq;#$PVY0Yl~bKL?;?a7X$oLafO)?Q79V_QZoyLR|qv5j}1og0Io!8^6D%)jOQ7Re`0e8>s}cwUp~w)JWq*#>m>V$QDK9=77ah1L38eTN553q@Vri6s7F=VjKuphbJ8UiyoreQKE0i{-R6CpJ0EE3KL%_qTg{q%5?0tWe^dFH5=-f`h)YP89w-;-WOtVsp6g!2a+&ctYWgML%_i-t}aeIU{CK`uUW;=?`;_u(>JwwxRUGN}?w7?Azsh3UjqT(%}Z3(4z}vKQqQwcqM_<LkS9^ZbX{QH{!Uh2-4ts=)-$vJPHa9M4jSr<d?{{?;92InB{~LwDmRpl|cLmaMBtF88ifWrjB4sYyM`qe$I=f=spR5PX5$~E(K1VCbo`-7VJ!0#GE~~>Pl<FO0`zB=~rPCKxZPkskSbbYA;ecsh`L~oCe6eNCe6h13IC3_Y!W0GMO`dC{E)Gv?_n<yoEsoCfHkO*7w2szCGuGC}ih9?fZfPHg6`h-nNZ~)`hTk%-2QT(Cu9%$}YE(1w=BDq|3*eLUl5K3z+^Y4<d)Ir<~9ji=6sU8O|FZNYdaFkK3V#l(hvQ;lj4b&z0n%awVnKCuX2GZ7sv3a&yW3+TmNopldaoi$9v3H@Ml>!gR6Q>ww4W<gqdWFcJ(U%gw;keH)9oyJ#yq8wigzOhN?hUA%itFl-sR*Zv6L3#YGO^c^?#s*P2w{7Z_4QQ;}YP>8J}G$A*CZ332yg}>(6I#NV%!MrdWPwv&`F~b8O&=|<RI<Vh{Wi|V)uF+$i&b9kxl&wjcNz+>ig^$FdOI=&ot8pFJXVN{+M~2H1l5V5kdCT=8u+zw_AkFtCV(pppa9BX5v)tkJV@JU$no$MOVY3V;n!`5MovQ|53oV^<y(2^uqve96HUk#H*1b-wwa_FSpf=li+5Q?zbtngJNH}kL)T68jw37zpYLZWV)H%uKP>;m%(zy*Bm3iGfhnByoyU(tJZu*j)xDy~kD-@y*VHwfDzkuIdMZ`tgKpx~Ycb}oER?aDL0#?gLUuNpIjm}j4nlx8^E-8mmj=X_qiHJ5cqni2J#-ZbU8*W=nXp<TG0dNqH9q@)#<4&`?x{{@34Z>ES#@82wdG2UdgjNBLCnSJ=p@+E2mZfDw*bp>*<}I!mW)ssrY$9fIb%jL$HDJm}+#n7t3SSS^&e4!M$moJ?zwnava4krYVT;QWFLOx91lM*uplGld58+2f)^~^rn<*+~J{m%LSC%-_)~~gwSoiz{tE^~>yJ)ng(&7!_m9mUv*Kuh$4fA7T9=^j^K+JtSZLi$HlJd2FqKLyB>q(L|T4>c21PRR3ixraU#ubbMHYaeVE<n)}b2)xFY|oVg(aev*0LFtFEHxqEoE55PrQ{hhBKD%lPrM5zsZjek?x=%ke@J?uT>we0QC*0+s`bQHkdB3bm?&rN_z||0iZT_MP^*l};pd3=5v}=*y!3Py6`OW9`-TxITtBZyx>tn214%0ZLz?V)acJ1yXsHp!>>kGIs`$M^4roBAkmw8#ydBaNSo5x;1AsXycBB&LNKW$j+(A>Lf{f^-1z6dTPga4X)vT=nRw9B?t1!<*Y5e4v?FmmX&phr#7^0j>CLF7l%H4W>UD$q{u9{uIt>ccqfMO&@nkk*+!3afns=O4$;iCGH*mV|#0u%;k+`DI_hiON<OgM^}S>y_-z-D0tO9~a=+^=)u^ADp=zYBN&#W)wOH4iNbDRIEYC=y<OYl~!g1yR9=s)W0mQGrY`nNX37LIR6F>F>KvR%SAaKoOIgpng}pP^cb-)YL9?pVd}|OM?3Dt6P4?PI539tx$Ie5k%J}Ho2YP+)j&V3Z#aMQV^8)CDosgD4vWjn}i~SBd8$Bwn+5SARU=44<5&lX+^kgT|Fj>&(o7%j9#+culcm>P@td-<#^DPskHws>47)_b+#DHR1*RD5X@{X505SezR<I64brPxFF|$1<F58naIxC<P`9f6(26d0XejlpiMpetS=hrhTn4fal8k&du%d^U&op3Duhf0;mrj=<CgUhAUVYv4Xl^w}Bc@1NTM;>y!1dc>3GmDebn|zF1Tb<9l=B-*qf|E)ICh?$4}%^B7kU>A+}CSFl=2#qKD=JIqAc`4oOQ}5*GJ2UXP?V_4VJ5rDe>XLPAY9+kt!9#(1rsCy+u%u--L#F^H|AGiFs+ET?>*mG`4-9(gT?dsr-PkPR28lp&GP9ej1MP(}nDg9Qb9|=*u|Z8E%TCb5kppt)>Bqa+#T_W*Q-IAvt7(Oy(dh`R9qzP#{qRIF`8+T}pcjOT1i!qHnrZk4Qb%*j-9FR7abqK(tv!9DM36+l-qST=uM+yjU52z-0vL;T*j{x<okLK%!6pz>B$TFPC8ddx_m%cJazyG;|v)4pzv8pCO1Fs2WIaPKT4NuvxsJ#ZEJ|4T?l<5UI;E;vF3^p5R`jX}7CoT)*&HbtB+)>*@MT_+;?zVgN{9+kpZCQmyO?p%mF8R6o@drSnFiRCUT1W@z=$s2@UUvei8RB0hTFfeU(tOE2p3UDSrxw4j_wQ`U%76!65Tt2BOHLa~yZVr-xt9(bJ+O;$%lEYpd?QciW()gh@GgghYrD0Sd3ixg>|E5@WB?Fg{Y=<~9#qB+Dg`p-PWs7HTYY&*3iDH4*VR9{>1vh#_{yXoCG5}HK(sNqn2`1G%lJ}#EM+m89;&sBs68f+WuI<pp?-<9=XVwzV8-Zpe^B&EfZ%WqU*hu`28TwR<-QO`rOokEMlHUYjmB4TVkszM~<v{o}jTI{HMVm%y-m}u`D7|#f_T`0u;#lqMb%eNYu&k^`bL3*xkZkpo#V)I@C?lvqISf%2-CCG!Sw)2GN<E1H+l@Lqf3)J_UrTRu|k$PoGLnP%SU!KK_Jny?xK@V?10h?G#C{JdxYh-L*L2}!p@;P%PF^uJ~9rP)o{hWw2Z+wfN+|kE})Y8;hMwcc(lGGZI!oX+&g&7g37gTeAZEf!7mm=o~&kO*-G)nAEB?&ghVkc}D62(fw8rRufc@Ki+W~hO90$dxQRN6xT=bA<D@T(&AZ!yy9lR_43@q`I;7ZDFq0t8sJ9)M|m$RRN?Nv<tnawWQX>8wg5LsmEwBJ8s+Mcgqf{J){zYTJ}I!(jld?N{Y20KY;eEzoM%b<zSzG|i~>3krEv_ZB+(epqm;#}$jRPO=N^{avZaDHbTqyU$rww|0rO1lc%8z-PAhD49nk(|57(MSL|fmfodx@V<*Ax;jc+o}`oGOBR?vibfiuw+BEr>d1I&QkP2d9U!WV8;ad<;DP)#S(#5qDfsH4ib`QEfKb)9M6Nx;Gt81yn;9p_t>hNb+yqVt3Ey)}$BRs9M3?=u*ZNM97GRK4B2<736;Zqfg$6}0gU~lbc><p5!uF$lP^<*+P6WSbLKOHtBhVxo4j~_nQ=yfd*7imu#X%@5>X%DCw$!@R;g1>mEVmz4O3iK#TD*{8FXL`|W<qJcKz}bAdWsZ0cZ=b8oEo-dO#%q@MZFF;Pg4v37El=)B4ehNT4X5$h?&bE*GHc65XvNCq#3CoQe!8m@X~};;_5RPHA@>KMWnp8Y?2`1)#;M4gjbz1h?Xm3pMf&R%Qu!<^oFWHaHt8=s!)$E+^9p(T%)cKQUK>Gl--nzMRY7YDU4H&xgaGishk%rTSP$6W+^qmAQ`=2rCj$z)2BNgYo)w#33!obN1}%wy+Pfp1p$RjY&5hN5<Q?POH3qzdVp$;#YEvs+W{UYoZ<nNc}LCll1oQol`J&xI4-fOX%G;^0z{X1c9E(q8rFti2J(@3!!&sbmA?{iI9VfVav$h{mJOV4G+86#pakA*vW|4uWQBEvt`e(>(*8{q#+CiecWF#Tt5Tx2oUtDUaLhlKaKBE8sDPmnr14SM96qn^ZqyUD@c7|LD;uy<i|Ji+CFm?FsZ-Qr=V~#kx(951R*{pcmNL=EEdk)xokcJ$Xl|YEc2+7=$w-R!?xKNJR~`G6sq?9Pn70;alS(v6J9<4}=yY|yjq)H4UyIXcn@p+6k=Pjt8X-Lu3YU^dmE>^oM`NokLgEsA^&FcEwzC6;D~Sa;wNJ%hry`)}<sW%?0u4vF&{2+`ws_3wH4>*dkpC6LiIiD8FJx7Kl%ZBTOUm0qrb%mybM|B)036_kxdnJ6{Tt4S&|pXq&egPebNnz~{h@W{aR{4gUTd-!)9wc-I+8mmI+6t?&5h6vX$_)&Sey#6&SR!Tiyd3eti3|L5gIwGExl0%JZsX#Gm+7tu;HRXfofmYr5OWwfVearianFNNQqZ1E^>3`sSO&CtIZsjO8tr1H%@nC9bC%1a4B32;Ve|p8DGy&UbNKdh$;(DVz>XFmwY}ww>putHfgCR9{12BdRTO-5B;tnWrfPiOF-jJ6A^G&X<f-^mywJ=Mjm3Re^S*%c`_AijO2#KdZVeo33+XO`W2HG(n=9gsCoMPWH;tY-+U&8tp!rp>*s35i~fvyxh}OlsX3IX3gnuG9Y|rVI+2?+sq(z$EFGK&%jT_;+^y{JPO5_Z1_hBAU^I4Zi>06(^E9EJ1U7?aWC7^G?`m0IiHQeW847B(ib|aqmQgj~Xvhhe0lYX)lVWM2?$m;_UO^6%v(FY^JD*~CCwb_i$bowVSXdWbn(hE{nNJAM6NN6$Ig=~6YS;`jw@u=>n7wE0Jx-LOy$TRbM3G{HIq5OuAbJ`u#zK)Ky5U0bUPQG!MuS%goW@Gf>TfguC4+5nMBYcp*}u?QF;~dA4_dM(UCciACbE}lvUftvi;0@MHSnx6TL9|Vcq^JuIzg6KS@#&D-0KqjZ<bWc8bqovlY-L;vAQZ1Ydmr>auY=V=g?99BOw^CSRjjXm!MUm=Hm6@F3}chX}tcy>fF6b`kbswg>MTItSV}a?&c>cl}k`pSRc6Xmzo(#s}RLT!38I2I<SLjv&vdFaVdhbxV}UXs^8T3Ab4xEet3@(Z^Dl~%QD(?mK2A%jxB7(gp+s<n;N5ErN}T2bAn}4coKP*RhMFoY*PD<-=j{UA&S}%nqe|}>s}WO6qD0>nad$oUsDMO>)h7jmB9eNTUUq?>vzwr0He&KgCN)?!L$1-w<O_Q2}Ot)`e|Hgz(o&8Mui9jEpsNYYW11pbS+oWaXV`eo`P8#Rf(NWL~C=dwaPtz!=myN9PHm0Nn0J&g&5Sqz$kG0AF7_sHE++)cf>^mFxAT^Zun{6PUZW%2ff^GxM$6a3_uMXpI5?x(eV7A9hnP(44dI+4S#D^q8|;+pgnwz??*_wOvOwU$9ZR%sZG1>vZ2k+f*sA1u~3ugQAdL+WxHr@BylM%x&t!YmT&umm1OI~lQL=K0y%qrYE+I96hQ<fB7+e`ZUwz}l2jH=UCXkkc9j%H2KOx<OMI&29J)*^8m)^$nyZqo8(U1#0?op7$oVGVLSdGkr|}i|B`+x~-lZvc3vhu#)8v+^SBn0)GO1UA^(Ll6Qm(p`2G(Up+7mE<P^qQinbQ@VBYQiwiP+L=W86fZPoQbE_rZn9dZW#C_K6=p3%gp^sYr#hRJc}{iian5(7Rmz3Zo&mYmoO-SgL(MCZ$jah?B_$3W#=BCck~1+BP0qL8(77_D2d_R#RAFWIO;dwQG~1PhP4dEvoV4#x1T5H*i_aS!JLAE9XEKBITLsXL>Rn7cZ+g)z(jsNfhwg6tb*H-9(hyD2S(P>6+4rh2*?~o0HXJq=g13x<!WL0RQH*0`=ZrL@<5oL~AM9?Nu_sgoPBzj$L0y(j*BZ5uw8aZ9oHOrkZ_Q2@$?B4&@LaI#Z722)Vv6_=qhT=sQCZZ!;&l2`&jAj_J!!<nq%}DbJWRTnBhi04-gt)-4<4df*w+d6prUCxGSuCwAmg8fEL6EA3Q}b&-)>d;;Ur5+N0$>j=gOkWvpqln_)oi6<`x6V(_@;MNpfOhDP{t=pbckxH@bsAQBF&+ltv)6>$a2}0UTfTg3&&tX@BOY2qIOS7x2ZLy|<P@9f%7y9T>NvoBGUm_Jcg5-exI$Rjm@nvWxF9NuyR*lgY5yNwxsV=Z8LZ3<{5%26_>p@3j*1h*106+b@e*Vn3=AdRQSoFz>m}_RE?)1EyQ+FFi+TjbwS5X&gY<kx@V&0DTme=?7OIB>Vka_~(lf?ZD!;GDXd37B)beK3%NET{0p%}Pj)8NaZXemhb(uk-SLlIp$j0B{dUBz1EBNllQZyj*QCgZu<k_Jdr5dPp+5}9&qjFL8AI(9{t7Z*D)Z(vBKkmOSQ{wk>ovqPlTabh)SPM~y+pwP7m%&p9y*D92r%NSp4-GQ9#W59y}zQSJ_`Nf8cGv(`OqPixdmS7<6tHCG<;q4jj>CAh7SF2wL`aD}-0}Z2FjD|uzbH7mv`k$<xK=Rz<+@^ihKNAxGf>>Oc%NICiO$@-MK&QmXZyA8fP#vZaq|OmQc=^rtKu{`3()|3y`jvDKjd7O5opa?u375D%7y>}DinUD}h~6-4u0!{gMw#v{H=5<IT886F>9#NmPAC;hsXaf%I~3(|3m?*MX$5$*>;ztO!VUL$=p%8th+kpSXw-?I3^tkrOR1NFl-ot#<?%%Qv^LU2JAP$bZFQ7<xbN()0M~X(EEJZ*X`FvC0Y#rk7wf?)PbA|LL8YGjID(6O=!Bp}geJx~>}sV7zz#Dht|8$hMKaJYfGcT~I4QBEI$7CilSBxP;66_SX=k^2f=?~pM3}`dk?}fA7dQ+rfCFDKv-Rzk19hU*%zX)z1AP&uT7-uXR6Gxt0=16%Ts6>uki0}Z>%$<MDepLBc@(OCMzJ^ROr>a&qW#pDMJ94mSY!!d`pYzV%qh|wA(go^#r@PA{jr{c(j&h$kObe}?NsR{uE(<}62`opDLPzU>SQ1p^xbS+F*<=1ul8lz5^5{01()E9iMiIapG*&IZsH~(gh_QwOc8hQmmRgq7zd2%GI|H2lh&(GQjE2?4Di3Sg~gx(A%49pRepZD?L#4JT`ZRiIe9pDCu!WEC6iWbbA%inaDtUpE~P=gOI?AO<0MFI9h`HvlI^0?eb3V_lPMdbLawHP-^ywO>pX*mm+~PHrPhBMsKD&FGz;!>jy0eajiu8(CC34n(W#fbtKV1QZZ>3FEJ$e4!X(~bMIlI?*eF`bH-uR5p7fbGcylI{m+;AJ08d_Mb*RsKu&=KF$eFhu4ZeFh(>bL2`qwlS5^t}&$@0B{3a7EtT`v6IMZ}L0hilj*msRT`*5~#PML~TsjvG$92)K$27lq{%10`Uza)3VT?OiYAlSX84QfQ=#g`(G&z~FJEyXFi>zK<|lLjAU7D5JI653n!~OJ^bJt!$Zqu;n_FnaWc!T@ig^n)})ZLDf7vR}_PwOtd>(v@Lpc@Bo8Co(Pom((*iMh2O2BtLA7k<%W?Ghv^?}YLMOb*eH^;Rtr_zrerE()o6VfR?JiNYNGhG_ZA{o<iS)0LP;I2q=%`bQOgxm+qU_6?_$B!N_U{^y7Ge^6h3zj+)%;f5;Tzk8VKOVK|;MGfKtpft-FX)hiPO`OBj(@af0QiQrygZyQZq^z)vUIY;CpKR^-iwmb%PLKQ%SZq1!ZWD%kqZ&-=XyuURAhR!hcGrw%q~C#2b_g<<6aJsAzMdO6rohJyP!TF$mm88+1QRQc49H6@mQbs-h8Lc2>FWcd-XQVwF8O>hLso_DIOy0Fh~tH<PeaT9rYRHh6~lj(hoP~)Ms>(!};sx?osiMjouuL^kFONtaB9hOic0|Q1R;4zRin9-qf3vxVTiK&1n_a=7C_jc;K?IJlE!JJM>@@;HU+m!%QnvB)r%b}{HlBZ4q#gH_XUZ^7Mra5^qOq|#CfU4C2L=_w+5#>}S3#}w4-B6o%wD5OZf$fx8`$QIiE)Ru8RiZ!kz%YVoy-x1+)7~FAk{o7}GAJ#tROV8UvIKsy&lqVa$~F=Udsf8yfnq)30Wn*ol?xN-u!(h>D>%?@$(9qvN=F2;d1qts>?>lf3?A=7(|I&uoHZZ@tuu&7J0UutW9u$$UMC~bgPXOy71$6_63I(F)Dy;d5m0DjuO1V!NEvz#z1aJ?=Q=Qx{Q;h?_Sh)#VYEafTTn!p`HQG`Lh(UQQo+yu2(AHO^RoIFu3b*#XxzDF>Xo><eM?2*DZ8u~oO0?oGsYM+iYi(Uc^x_y@UR3&%JhJbO`2MJi=BvYSd+8nQE1d0dZNja%tCh(%T<N3l3WmrUdm^cCvl{L4k4$@BTP^+RPR3vmUm9C$f>YE@2oIxpbexdqfY||Rtc||CQ%b?cD5<>6%Q>LL28FDr_t+T``|lJ%2*QxXBE!6G|hhj|6oP%yEiNJ0k99=LbE>H-+h)_<)|yTxz9d%0Wg<0S2CgDntH;cbeO1H8MvV*XJ^o_4Zzb<^>oQSj9y#5%1r6~Bxjx}W_jXhX)1tf87gvZG4iNKu##;F-;1FWPWh)^bKG~6Q_TrmP_A_4y)=9*mqw}f8Ln|sbkz4W$ZNqZ3ofkz)wZ!$a_@zv2r|$tD<Jn;(6`odAQKRJD>$Ioh=OGpA7G()%ger#r(w{_M}d5rqea8wbf&bMC`D-Dr|pP{5MFge+86tU2%OS5@!5Z&zV2t3_w~38^bagoYApp>g!OQIr|A$VA4pR#kQn9TKOX-d6?ys~')).decode("utf-8"))
_HIGH_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>bODa{Mnm_hFhJP0}}x)awyeGZH9i8|wiv7{F^7FxH2$Z^r(2%M{uD-mA#Sh^%UoGv=+;YQ9(Bl^Gcs`Sbsr{M)a;{rzvho&3|!C*Oa0_x|lKA8$T={&KrLxm%t5`>+4`umAP+f4+YF`>((K$KU?@>*t?Oet38PzuJfIzx?%=o1fnOc=P^bb@JxJ?qqe^eEsQ%?e^p3KR#`@Z@+%M`(b<Y`DAsu`1;4~`wu^ztk(OVf4u$h_RE{khrig|-Th-V?bye6Z~pw{<Ka!~N#A}x*=;|4zHjSKA8tSYaQ|ul)#Af^AU<v1zdyY7Z28v5$4y=Z8Zv$D;nQ*|Py-gP3uh1ZaNm;qIa$y8`tU3Au8;3;-fW}sME!aE1Ms#*yUAN0{$x6yO*`(t`{}S4W_^8_so-bn2ybte?>{V$o6p<Z<sw>sH(xz)>7FhZ(WehzmW!xeoPYYioiY1n(K|Mk?cmG@cri+c{=K<*SelPN`nEGCUAN})FkJ0RA4g&Ot8}`+{zH=kc0#j)$y*-A9*o&!IGP!2f1}UX!?@F-n>}~A^A1DUPE)Wh*TUfjHbZ!{^0Q^u1#M)}p_5PEV@vh1l)uU65e(tO2?ORRn>T$B_wU$$_<Ht!LLa<=JB)kJgCBlLCw=Vm>4XpIz~kRe-Zb>N>4#@{?BZ5A3#`fHFf}faF;88dt<Ls+@)j)Z5%SZ<j2P2`Hy_@=-@f_$%b&KlpWnTI_b>A^VbI`}Ut%ng@;i<+2amV*q&?vt+B+hP9|u?Y#hqaRzUcLD%<r;~=XLKkwf{P85@6mn=HtW&2Mf32X8>aa?g`whhox<q$-EEK-e!GF2M{>+hC#|)75FK8AR7zxDSaUG2t@m_!yk>CTy&t~L6vM@Wdl*)JfDB!>GZk23h<OZ4tmRm^8k$d!y{W`FyH(wa6)X$ynWW=Qd5=SW>0KbzdmjJ)8u;}*ih#x$Xz!KsIAcU4&mwR1wQ`u_`CgpARFmiWOpuToH7R$(_-I_$yv6=UcYy>$o(5Q0M@`GU_QbPikA$%u!jsY!dWRQ*fW^icw+dc{#I)Cpgw|;?OM0YLTLYQ%y5EDcmOE<S25@<8N$MhS@+1ZA#<-UdVSIBi~guD(ow|`_Ge6ofV_$n2fVORt$-)dzPo`Hn2)W2UPV{l0J-|2!kOh+L8d&Y&}l!RI`pCo%(w~0=7*cxzeF7yXWJMMjz}#)L$&Wqafqg4(Zl;_2d51T?-?Fl=oTOJeaF7N)f;qVEba$oI#M}C1wgOavOBEN$3Z!Sq2)n8JP}<!)As?_NRRqI5@+ZQS8=|;Ahi!}xodyeDEI4QpNv6p;aE-=_j`Uu&%DBH)U{(;Js2^cKHuK#zTe*7{uNj<CD@PgO0VeKAvgAPIP}LF7&KyicLW^p3Bf+=?ljEECBRp`OJl^O3e_FU#F|<sQ!LKI+c;R%wLbPA_E&oTI1Pt<ypboH7Bi9u#-F>qljR5$S3%To>+5gLtXhQV)3=6J;@<5oM_7mgf!=wXVE8$Y>*GkiMjM|icDb=Fpbop{?5=QpQiMUW5s0CJj#tH*roMUx##F8qhE_~2!QF=s@9%S!plS8+pAQrC^?ZDLQnvLD{ygrj@wIexYUUv0tqdX(Er&X~6=Z{VJ}dTG-cN)G%E7q)r9jC7>0_e}h0+u;KO~O(RqksEhU((%>Ap)JWvz|wrbwBD-Zr1gc;_}sTJf3)VAEyb*=r&~87D-xdA3LQE-*UZPB%LGmZwE!8?a$UpY%Zir%nqXFY}pdG(6ywEX><uSy3A^g?U|y*a7ovjbnD_xm5;JjBQg*<hW^0upIgV>=GR;LFv{YJve9sxSH8jrz07PubmB0@O6932S4O+gL;;*$%ZM`c|N^oJxF&tO`)XZx)g3;;MqRvWFUcH{%?{Lc*gYK2c}30dP0cnu`JjQqTD}S0DvVO+ba<ML8o!N7|4{^2F6Ukfr)?728O{@#BD5skzu$P_mtT;6=MTf2Th2!ktnc6yzP8w>8!;6%SW6-;l$+X8}W8=ld&W(XW82T_3ch_%5Bj0|E%+l4J+*$`;(%hl!Ckja%cZv%e`SaLX2tKm+&L!?AJh8U|{Q{;o2(!Nkns0`l*8J@37y|puvwu#E<XZ|9S3HL5~ZW3Ginu9=?Cqk$tbT9822YugI*^O+lBW7kFWiRRpZT$h&B+ZH3~=0jWAZp=0wES5tp_dN8vs0M<wFzHG6y=IYF^Cut$dRuUK*Hw}Oc6rhmDA$zxq5}53xQpUBqcr>@Ngn(<5j@Gk3SoF;3!3@GaXtMPsfW=MXTwI$i_KM7m!W$Ck0PYa;f-vvXG?a+1&<-SOJ@K7kpsa@-s=&{yBv{j^L3nctsHI?P0&A8GE!qZPGj*H6C}_cR*+3JgE3f4lR}5v)RY?G>6;W)yY5%;ES8z}fjNctnm9z7ZwG7$0>k92h^2b;g4o{MjXM{%XXWeUv<k92;eob@091n4#irlE4Y_AuUdiL6wV>PBbXgH@xUr^2Cvcv>a7(NJIU};A3J55|{pfE;jpXuH-A@O=K&Ya^t#G@wBKZ_OA_(EqAEP!ndL-wK~)-^bb6CmRIRe~Za$aAh>Gr1&)`X&KZ_{KFm$14z7*cA|jf8qp`87J=CNa$^Pn7Ct!m<SE96<TiP2{`x|O^ImP8l6r$cf|SV692O8P336X#c(B90C9?L5KfOMbA4PY5)xy<NEU*nJ?n#Q5^lyMSR)3`HIGXtW)WYNuR6r*h;2QzmJ4kIS-+2OAkLN)2wQez435qmKH`s!wWCS1YNIx!Rmf~U&d~5?)eoLyyGAwTsF%>Hf;Qw6v<g_PFQHkl3v0mc)UkqN`uW{K_G7s7mFTz_gw~_u#F3xD?Y=9odGNB8d{xR}34#X}k+|aPRw!h8SX_6{qb><*mtKZH3xrF~9}X*)MF^-QW%e!!kBWWq+N^`PXEu4MG!)GW?VM>kT+^3`VfRj1Z|)+J3=bUH2A~8=w*&C+dTrbR_?2zD;qQ>}D6gspntN&72pY9PBAJ3Mn2+q`olZbyqe=Z{k^>m!RO8lOp-6|`0rYmfiy7&bz*eOmY+`og`p%#Mprr(ws^MJ{6r1-<hhV65U9wU3%(!W#&RF}+>&xt+N&i67?xbcRX(Q+z{{wREBXZ=tFQ?~|zRWrvSMgb280qF|>(pc|nlp^M@ZFuBLd3~L6jFtJEihqZ$)T0SyV9ZZ$tIvmy6qADLc<)DNKI`@T@aCni9#CCG|?iQ<Y**Sp#iik1Swmu0HBmKQNS%S%8*NNK${~W<exU`B_r7Rr)O1kghM7T1u2OtKU+@m(J2rI^q!`hgB|NR{Q31%<XQtKPry$kKR-*to{m&SU#Rt`s~}2|%MpCt+Dg-&>RG<ZvQtx47}+-MhK$@@TWKv6USQb;)KoB}^}NuSyxgeIN$A58)5DYIY1RvKsc1u}lU<|hGJ&p^;KNcTD9Ig&X$)B+0Cz;XER=L|<OL#417nd<r-LmVPUz@dIH1LBrN<n8O@0#&_Vzf7s@=nfeoTFK^eVZEP}p{~x2nsEaI=!c5T$ua@h9k-2N9>0)F*`wldpG9gzH^U)g6SP9xcg;)y1kVGUJp=_XBG&&oqm%VtdR9*N@|&f@EC+TnxYH?A6Nhr|b?o>jt(<PFGVZ@cJ|3R|R6_Ch)*Zc*@hRBM%Vj{9vsS8w5H4K9X4803c{2*5jf=$A^6Y{sYy6i7?)D2Clm0SocS>p6pVmoiKzqZ#+zIX%FZ&GbDvYl3=c;i)`PD?V>nL#!#Fl3_a9*?5vggxHAxxV-6K|l@cDI241Twm|&o4?DpcWLY1$jIU%AydXOVDz~mWNqL!*EVCWT+oDG1raG*g};cVmNH5EUe!lPtt5w41m<f$_`L`VvabUS>MAW#XZNQpstF3&i+AQ+?x+@W5U&Nwm07jp&iw|s{zk&dC5921~O9QLSE9~Ltb_s4~Sl88beTzCd_T)k1$*fm=wd_(KfhnfgxT+~EZMhs2l-fOn%WA2*2UgD}rXnAS`4S+w(4!J^|6zg&chn3tVb_@rNE-!Wp-<#k}allu-^^!H3l>TdfkqpKa*6S(N?>=c8kQ*<bO=4pN;P7Nb6J~#N=mBI5J2D48$E5Wc`c)`epRK`9h&R`(O%D@~GDQwbbue>AJSeKaT$C~s74V`H(_%CdNwS6Qg=)%9yGm5K3u>MeDjU)KJqC&BBpc4X=_CiGDTeB}wwGkFCYr^9Zr3XtV0MA~_Q(0%AO~9&ZFxjC7DVf;wktLijLSvQ(oB*);{*>YKb<DYau9=>oJMgo)+kiofuTLfHcq9xDv+WGtf-s4G;o@~Ea6WohiW^faD;e!&{a2T$izUn;)P3D3$<!ZVv}gw#LCr0q7kcdhdgoAE(uaF2GkYGRlf^hrWQ@6uy>7v;1g0rTtTl2qNruQefQ5DL;|BNHFy8I@#-T0;QWt987O#V0WhB>?{_*%PD~MIhmI{R+?vs*L`HXi3IRviEz!j-^k8^l&Wo8kaX7NyA$BY6X0=IRgrv_c4$FHy{4>k=80y^Unz^>nMy)m=DimU6@YHr3wO;2_Q>%}yC`o9`G*OG_QiV|UUMo`!-g{tPWdq!&D<gU-f-*`?Y8CMMMJK)DB*}cM1VuLJfzprze@Ak@i{-I7*2(g4a%@raRbaH9x%ibA)0`2SQGj=!3ZW_Pk5;Tki9`=zO)42Bi6_22j(-z*GZ)zJdFlQQvZG!^fD%EEVhpb%0iFdX)tqFof2hIclA+ZIr1Ck@8yum0uTY|OOj*~M6A0`)C%h<;CatBk!@9pDj-Ad?$@AcuEIDA_wPB&j0ZDBuNm))2D{9YX{jR1*flh;G5$L{|vkE?H#U1Iaq+8F|0^1m>{A~`1CGo)oF<a9@UuA+G;o-4uG6?lHR0qTsQCy!nTwOVHMXf_Y>nf-S%Bho3Pg7>yk!Kl2g?5uQZ>4K_b>xX$W8Q}gXVFjFh}=ri;pVv`CH28VI+spb<H^|)ExAv;^VGQ?p!*x}r?*~Ccj0&fy*YP_11AWE#GR!<%R$q$5!k>yT!c3mWj+m&;zhl=5*8i1co`ak#Yw}TGyZ+wlwAq9iU{!V<4s$LEQ8MI6XdEZ`g|ILLflLOC^@o!O48D>Z2qSB65<5)b#e^aHG6ja(tDq3J=MFNYCEEv_NogULv!<D==+92&Gi;j(58~|P14zb!|nx(>zV;o=76$m6P176#wMlEJE;TR!TGVH-Gi4_hO=w=Qs_w&(|4j+OiEFA4zfZXaO-ypIZzmqy6yv++NdTC(~aWc?r&YPz-JBNM+Wjd^v05+os2|~y%K4iZ$dzB{tTw{ym7s!7CF&aAC-K2wz+{h2xFm(^?|tx`MPQCctGO^r%Mh4x0dd=0W~WdHogRy7N%|zo{Sz9NC$<}$c-REZ%39<f&q&#a>a{np>R?X!lP%gKtHf#`P=!6OiWl_l}NdYRX~IpgX5*>?nMW+2G@41v1L<|#0+l9xBbG?LMA=9npel>#d{!y7_}3Ch-%S;O<WLU)l?H-5gN!8Sa{`oM6L~t*0H<lIoKYI=P8)-F#Y_jO4Rd`&v!D{13+xdA@1~TQP8uDD$E8OU}i7J4+iF#A_g^~M}!5omZmT~<o3^SY8a@+QVo08N!IR49A!lT;MtS0FSMe8o!&W6*#aJys`%JP{MV?XMA@zt;ZrK9rT##@#N4S<*^jY568k(6TlOhS7A>P)=3#xi&9YZ>TUiffYZ?T(rBxAIW1JaPpHLOpXL4mVI2tUPQn6zi%#Q8z-0t2ux@&a%2p9T%{bf3Bg+hgwMkNO>3dW9GMyp}93kOv!lqxyI1yzIZ`0-|D;$8RYj=J=#v<_{x*}y?2wI%>olEEw@_eqWLYXFNzQXtgH#HrKLNTVIR>cwGHcATFWBqrR+fqS*H6rd((5|Po^pHBAx$C;~E3V$>?-pzWzhepf?=vo{gDlOylZnmBzvb+R>`92?3+4E8$WkkvizYB$iXVh3sax(KGO2@;oJSfGeo><E;wiB6(j0i`qf?ZjIR4dxGBT!^^DnOwZSJid-a;etGgQb!QMIAOBhT%?L&Lsj}ysG6mQB8uFrqx%%b%e%$M_H2CW#a_?t*LH)UP^1C0u<=B&z4<f7mg5QB>7IfLrDUA%-T41iW7KqE~LUUY|AZ|(wu1V!=9zYONnSY^DN6L@r+~1j7<E|cXF=oN{SzC3+GEkC>w!8=pyS+1YQW3M6Ewnc9FQ=ZvJacI$vE<aCvd(ilt?g^RYGQPU`0~YKi1f2U<inWkaotA=QyWU4E1jJhZs|Mk#`vcja7kbJ+@%G%UTz(}qVjlh5MFz<17tFP;u;=`m2I@J$KJx)2FGO!AaT9Wf(Q%e5+80Rdoh;Y1pxqOoFdk#n*}W30Tm3K0UI;CULWafIyo4E&n3Kmn6oyzLuec6u7XZL{R4d4K^n@fCIJu56+)4W2+aD08R_N;P@WlZ)e&HNo770X^KMG~CjqTF@G@)I_+6`<(e#)ml38N_3Lo%n~UrVy3F{ktjDlwgXp4(uvIzG0h4Si6Ig-)~cT3z~ZVU%1I_ishtwyiYtp^6ZVu%!1Y~0thOW&WtC^pmipSDFDXK}jOa2ABXWWOz2NASGz9%=pjb&#RMc;6b!?|t2`kKpC+f7)2YhvNlurwVtIiV)=XVMMs~lMc#}KO|MlPQsD!k+2*Pcq1^6IgmWJ2X7BGDq|sbiQMVd*gJPtAGYw_9F_n=P0t<K(3lI=vNOip0bd-Gs|f(#c7-d-JBK@P|K_4BFGU`Vu<CkTV86Ougf1lB;!&)uMo!$N{~f<iZLnGwZC9KtN6uUI|2DFAB3rjHHcm_lg?kE&eW2DAkMivd*Kkfv_3s^<9H*%~;KCfuJc3Qiqdt*!=~T4LTktO=6-Ye)7|j(qK0*{v@i(9IyTmU^OW&H52G73Hq>e?7R;lbJFENCYxUBNAO!OkFoX)r6&MA44<yEzSJUZk^1o@S&;+F+^%}?6SEf6{9lAarR12D&JG2PBjyc;-x$43Bojs8p#r-_l!l1D<(w6q)gv4X7o9b}kQJ;7-X;~O22}r~Wy5V{HANj|xgTnUqe$kjU8p-+W@#ZhDaWjb@}6gx4yuKfawm=YT#RoQEZ#~Er8-2slA4xqSPn4&a;mW&I3=C)J}ZHqc7^!)&I!z$3u9aMCZo|4#$6Wd*XU`$aVV;rsW1wGM)M-!d|<0wK+-0uaiGJ79G9oD#|2v1&eGDf?eg5Gxo7C6iYJzyP_3PN5F_!M4bRA&$ke>*UJa~s#)CS~P~0rhLDAF8o~^!F^aGh2cAQ+lENVGiXj^m^N&0nH+Mg~GqBs(r(nb<AVdeq)noY_wHW-X531Zb@G?U~(V#*mRH@Tj$$Nh~a*UKo(#csD<ldDE^E=V*7aYd?8M~0ron=)`qDZ8ns)W!Aiq(rN<B(~yIM=#bL73Q^)(#UxNQ!*8krb!QHb0%XBS0zJ@tWsU28ZA>AO%T(A<oR9KWVopAq@>dhl=+XmKeH%}!y^w0*#aWWxBW(e8`keI&K)Wz<a2)ETu^q-5LA(#?E8yo-&c!dO`dAs!%5W^j%OtS*H9|lsFW+u>35C-E1OfsfDwzL8xwg}o3{Ltq-mTyT|MFMiI(AI-!)5>w<x(MAsi;~0IYUVJdp=TXyw+dGT{pCyR)cgQNeE~8Fl#t#vz=e&YfQBK|@v5J?L}Oq&e$CF;81%v-Kt+rg8WA^#4JMW_Ti=RXoRK3(vzZ;V#nuoZD_LcB<4fkW_ACj#aF0RjX?yNzrFY?+|d+^1Y0ZCGa!~nW7!+E{^Eb0^neZb&P=`^M%aWo@K+y4w+n-o{wWB{1)Y2SdBFbKg!9p0!``6@#oXz+*X!{h`_@>8Z{3Y-D4{rhqP{8J<LH^AqI2=nj{jcwW?h?El*Oy$w!Hzb`dj3Oo+>a&*#qeL}J0s$&;u~MHK*<eQR}q`3i`gDe`U7NJ0$cq|qKlJeuf#TlJ38rKR#)^Qn>3dBKz=I=x&l4x>tW?Mc5{NioMUTlN&(mZXU6IUAIFluV^WF~vB(Kp78ayEcner(G-*nSwDH#CDv;N};lNH&JZ|iXFA9`7xnxF!BkuVWNO2Z!4O_>7}GD%DRl)hibxzR6HU&Ou1b8(Gjx*>dIzR`GY~2V0W>AsHWxFWdoi4Zp&PvxZS#|Gsl%Ja}>>w!U>cmuni$ts8x1#9IZ0F5T=J=z&@;xQ8BZ>oTW57y=2ImK$))6WEF6r9+gC~7h<?oJ+tHx*h%!@68q$OR2n8tV3rv-L7Jmqry_9=9Z6nGM$Mw1FuDy4nBKE8meS*z%5pNtp32(R7F?QBO0IGsnNIHEA%V1TJFVvxaW<apm*WSME^i9uB|{yIH~?8tYRlGc;0W(E!I}A*q*@IXGDF-=B}pmqRE#vY>wy|_R5CJi*2PS>_z0|WgO&It=jr62pe-}M>0=*?Vk)7imTKWcgG|D8YXUb?9VUtft<u!I0D-BYgZk#mQj}PDCh=6vTwO{P!E<+6=V4i?nAy~_lTz8hWg$2T%z!y!YOMrueueDqK6-Z|iAGA7YWc=A36<rg+5ptG#hyGXvL~flAM&I=S}^U_e`@}um~v02Q{(QdtM)0S;X(ztM80<h*<G@fwqxRwrwDB{zdRNv@7hs{7{e=M^t=tFu%q60@vC6QE#%*2Cq>F4fwz&uy)&Ua5jm<*8p?R84DQ&>w~AqP-i5{&Ypdc}7|m(8=mPM;1{sVfbFj72<I7T#Ogjh?vSCz`8VoslCIVHLr%IjylG9ipV<1JQSM1lHsHNfhT{|y<1!V03dpitl6BBmSmO3*aQkv<5PIF2!%^9Fk+Q^u!{)9F}b7iwdId~4|QP8fmLTH&tdf0R_bJA#QB6wca%(_?D4T`f2c*%#05^u^l5Hkrwgaev$4K5<b<pOgo#&LCso+#(+=sP*hF)e9p(U5}(gRlt}p#C#!fJr`FPLWj#eRxe3&V!DT<ypNEzuOW#q|CD{Gc%`^(SkDfTZFe(L-)wKmMR~xrP4&{a<3yqAHVka_QRs3iyFADR9$|+rqKdpAM%Wsm~cv{i8UhrvdZYg$gbAMLe@Z5>nx}8wVG%zEe|YXm6rGPRYa3$v7pWQ@(P6Jqy1uwgknckb6LM(<`*Srm8>fr!YjJzzGU6hSiTGnvbq!&Tfg8+ON)|dbyQgxq@!eEm8ho~7bNqE>+laLEGbj%ELNznU)_N35!rTIXPUBcD9+iY!lP65j^UOPE2NIe;86&3X@h`n9t+d@l1y!QR4u|L#Nxf8q1>WpPJumvour^dTZtWqJySKQTvpyubZDglh@9tStEi5m)bVu`*QsRc43XCCaHLgp+O#UFv^)k*X$+JLG3cQp>DP6Lky=-jlOj>H>YBgad3aTU%Y+P5HC)g@H*yf92R#RqhY&TT=bULsmuK|6W~pCQWxQ7s<V>WiD8&$%HzbqZ3oqACsx#c{bE5()s{t(8r&NKYq*^$WavOST#bQLVXS5>{%KO9#k-mP-J;KS8`!1>~Z!hv#Upl(jSB$ks2T!2N#Y%RCKZ&DWHE(vTP##yr<4kiQ{3YDyJw!c~YeaK)hA7;ybvE;-DT$B!2RZI6hP}^Qq0K&*f>&S5boHumXMsAU^ph;nc85?IK6G)3YHu-}y3R(?<;xgIt*cV)MuSLKCE^>)(P(i#J<6ljsIALdv#J@zO{EL{<xsUJ!EZP}OfFK_?bLti6mvT@j1MXd#%n`H<y8~y@rplFRE+`~1qD24Nl{;rpePoxHV%2P=#n~~nE;(zh~>OCBeZRSuv4ZbtjhHkE2t|`!VWn+DQKgo{<?TL$91+An5@Zn`6kiDP+B9c3(A5ObnSK!JkLx4d7;~o)Y}L$@S<|0B-?J=Um|r~+ExwcEY)OI*pWhxXRq8HZwJ7<)Y>PHvubeSPCIF4Jhhse4{dfW<C@Pe0&kBkL)8hS3qU2Y-Ux$!*_O#Emm9I|BY1y_xwZM7%lEZXg-wSoY!4jdS1+;NZvoqiqA|42W{@dkR9Y3SF9|J88fcaMwX3>aN#`ZQX)1$h^2~BBrxcg2R}}WeV%!WjA=7u~(em69tzqED!lSiP!Un3j6BVJ#jM`;~RvkKC?LMJyM$RdYq*E>7u44IW=Jf9PnJbhEaq>`gvYIip#e8U;{HR6Q+Yl0C*WKHpy$#f13C34xsf0P5tFz@=iZ~@DW+u$I0u(G`JgKFiBxZnEyarb2g@_4-V!v2HGw_iR(%;0Omuk>#N;Q|ML&YTJB8YNYEI#125#KY%Vfsq$LL)EXk8)R;f7)qy;IxO=eOc0)GA0uwZ&3?|iCQO{SZg3)kxDvt1mxXWx{Q}~NFwtQRDnCGU~b{aJ~h@8xKup-wnPitBVc<g3g64iW1FG;Xa`8_o1Ee`8ZDZglIOevYD{JL202ZC`-nRNcHUJ5WdcOp(IC@vq?%@FfIIB~g$)sP$z)?siIURdhw!$w3dGejFH=`YRn_k;>7dc#al}2U!da`sz_p}+e?TMCl}e*DA7H1l#%t00{66M<L??Zj3bw)<tN=+!vVbd1Z`4~*Zdq5cw0o)}WE>ngUpIN9TEoU`6MmOEdz#`tGcML<;WD~OC5;lMrCDj6tcuT4PfI~NuXU>CeL^1b#62zbCpjFI0ELz&krs2FKp{7uKIN$;vPXFTG;ah+ZPb0^GVd+_cK@hK6Wd8%JZ=SBy&M-f+&vA$5_HYG^tX>{*sj#7qmP#~k<!%eKP-qA&oP;W4_3pL*f&LJS}%7KME%dG3LkQD8;YLmJtk)%Q}HqV*NVEX6ackKu&2;!8p9{iw)E{t<W#D7!a@y-L9d0G5+4E_M!6RTx{OQOJU)`!F3S^$`G4eSW9KR?2GO+6U1Q2cgOI@ZloEJRN_XMF>#t>_OrGc-$<`19TW-i(5v{bDyRom_z4r1C)62KFA3pZ<GW?NOP`N=sAD#w-s}F6agA=+=X$0UD7(8j?$n1b?VvD~a)5L}Y^jR8@oFdo0wH^BXH{`z--*`)7p24P0$Z-4n?jLvm3-43V%>')).decode("utf-8"))
_COUNTER_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=UwPBm+}K#n$dK(2n}IMGAR7b-HV>1$1^eIQSR#3OPjz)wpF`SS_{juC-+R7KcXf63um5}Y@4x@?x4-^z_D{c_{q*VG{hQz3-+lP_>2ZDbbbj_9zyH_2{rBg;eE#^i-~af}zy8nX&%d6%efQ<B+J~P${pGj2U*7$EcYk(%_WEIScD`)B{_u9aen0uchxPi+=dU+!*LNS!&aY=*|Gd6`_~q<;vHSV^$A>qcUVq&GkE^Grzn@P#_Ws@LKYx0^f74>pw_ndT>kl8lwDp&V$B%EneA<0A`*1iAAJ+Hx`?p@q-@1L=<W-;{)7S1l&8Gr2VD`Fj_FxZpE%`Dhi-W$t{EEEm{r%nRbu^x+KimHR-ZpDDdF#u6nT}`EjxXQ+vR@1beSMj!;AiOwukYsX-!G55kL$<zBAS19xO(8yUCtNLhlfw|Mbs|NKmGsCIQVAPJ2sW=;2aL{Y?Su>dwut^G`Bx`-kFoGTXVS|uJ)zdQJDTJoi4Ed(By!f(5ztcmY1;yV>TI%X2#mz=ri^*?sVu5o;%-p`yp(nDOi^a;cx?+Av{|7*>cbYZDi4*lTY5ZrTSRP-{kWMhVbQt0dthin?8uUckDiVK6^i)58lA-$GzvlFTbRdKKA)^!iRKV`+p~I8v5My!&i9h>{hu5tjXjsH7<}bPo1Bw&h|Zd3+DC+`DtTDjA_B^hx_~W>yN+vY5n-|-Tk|NJv<Wz4PN;r#u6#N<4AL`y|pLp3HQ*>5t;osxXLe|3=8m^UjN4Y&ilBkd$+0m*J+ag^R6);Cq_6}xD`JG7$a~`;9k8fZOcsNeVFz(>ti~Az_B+BQs%0_PuT<6SfEeo1DQu4+K(OnXx!wY0~HUdWcw-`i2COF{1Z>7&-GP+r}S~qTQ-~rVBGH?*&2iS=5K)$Vq50zvmTe4ssuMXv0?q=Y2%+J-}}IZT44Zt(Pb1MAXzju*u~a&#W6G|xSdn$pl}UlhCnA&CtVCf3<QKThL=Y1Ze-y4{<!WN74S0W(bQM~Z;9qVy%97UqGX<s;o(+W{%8tN131kB013`TM`XwW4Oi*VlYfq-{o^2KKOXzzu_h)JTQ7F39t6{asC;5+T~^M_iZ5=0BSn|b07Lqshnd|~F;F~6$!R|ciT8S;>`o8H=I!0%zeFAD1&k)$(OrEp1dWDj*O%fDO~;~#AJ7g?8$jGK0lH8SKIprSJ-^j-W`I4i8<got<yZy)M-G<VevNJiWgo7T2YvrUbg4|=H@B~>=<t?cL2oYbhDvz2eQ?Wh`e7jacx*4ibLrSfmtXe$0gdlQ2Yo^#>cv$0@bU3(^V9nA@h^ZKD8-G~B^EXuynXT11BK)<ro)yD2`+8)BiT2i^!QmiZiZnvhp+k}B_oQ#f=-)b8BJ4rV+v7um=O<Vb*+!xhutNeKTd;Tw|DGh8)7c%z{q2lzcC+y;wp&xZGHXR%&LutK0P<I67g*BEy6z&sMF5lDmdTK*l|DNOkXQ%b!FQ$C$dyx^q}2oFR%K%5g#8=x`YX|EB-NczcYNLa<4D|VsZ;^9v<$$q^Uq7>gA6wGxYg@d?Q2x_rAClt}D}r&f%ms+%iT^7{nHt4{CG)$VTjTa^xYeL1)0w0a-tzZ~4(NFp~IExojm=s4IY~J05*Zqc-lF0#_24+I%X*kLyBM5i}8?nEOu^unvKK6aEpf7`wNEF#_$JqZ4g@HdOWk8*B8*92s!_w8-u}_FUsp0oP(?r5?)|x~k-$+CejjxWKU4DmSiRj;L*M9fwks*-ZQ8(olAGz3~nMl;P<{#%jFEc4j~bC^aX8uQPLv!vyLH0=)A)?f1N#5iO_dl3c`$o-)gM^(;k{2Ta#HPwSO21p$8DMWbMQT4O?m9j&{3AIG!UQ>Jy=zPCL##JT7TwOi&kZXLVlbz?ESZi9vxw=&p-?GZrkebA!W--;Qo%qB=blpI9R->_4~4wE^qbkjHL$aGH+J!Gm=j$MG>X0{u%F?X*?0ZWhW*ABt%Y@MepoDYgYf^P1`5#(@p?cHF#%a1Lla{#mA*stsf9#>x}rbWhnM?d-Q7JCtv)XbE}*WNhrXO>4%NQR)s&hC#rl)D-$ZntTtIBsOvZ+|O<Q8OVS(P*T6P;4J;--;<irRcZ^9fG5Ae;mJD%s;=o|MSbri`=31mwC=y59<B0rJvuoSmrx*$*=%>D#7BiVFB*M=rc$tw_wGAtu4sGSbn7$C=!x2k15~;j^;fbb828UFh|SU^jxsoSng(WdSv8G&+{a0R|pU`V|kGyqAlNIBKw7nR^(%~t;7drA5;$J9XJ_mcLC9|_5sDnXv<dxE{lka#C}Z9ef4nU)~aR>oa67+5DYM8U>*w}s`=W~lRQQ1*Z~;xyNh6i(jYhxXd{5TEIU(<KC$gd95hK9P_sL=En&=>g+5d<k~i=ESyn^?^d|yfR3M{lHG1wX!)g5g(aZ2R0G;k6Pd7?9Wlfub!?GtVxaq6t<|n_?#GsDhzXMw(bKeQ|)(dIs-h3XUYfK-_sqb;`8%F`={9uDrc68+*_U17%H@{uOdnCSHN#lA_&i*`Pl&$ch0u~l<j@Ds3oCaWNc$l!(Rs^3&-TLW$df5Lmy^zQ3lxQ36tYK*~wG7d%mJWwXUMo1L*t-(gQ}Dvaa0w{yiAip?um{)-l{{z3<!*gwV5yQVISAa4lBDhgpBDU0R1wih+Yuzql8Pk%7npjWi}9~I6PJ~>(3+)6z_K-1>$E?<&5zw;dkKi#g<j_%*Uu2bl#pTC7g<c(RZ+t`L9>7fH{_M49IcbJ>Kh%b;bed@LN=rM0<~7j34bz_P<E+vn$Fh?*AxCsC0t)uOOxS<QrMoFc%~>$u(Gb7`jm;4?#P3F6v8N28GUk*Rade?{{(DTi8&4<r05yl+5(Wik@(ax6+iS~ioqN5Dm4Kw%k3<tc(wjC7@+A(#At7Cc9{BT))W|)SIU%40pVMhkOIY$G?$o$lgUa9V0oRy4qlwiGi@UH&uM#G>Q6CHhMNH;#6t0`ytOy29?s>HehV;;GhesuH(=6A?Y{~k(Z#|rE!Zk%JP9x_JU3A8mVwWiVfIF~<)GxExxNnmZ?$ujM=mxJ4u^2dw-MaDAE?uFqF}ooFZ1=taN*fNTqTpcVTTByN6Wpw5)Kg!O$N7#Ig5C4^eop!r@sVzI@HG0T8ipd@)f&(N3M7ZlEK(~Y%~KZ?1AJ^olBS`$rix-rezM2BZbw(3{ByDvGw)KLk^1oD{5p1d=eiU6P`Co-hP%w8I-WSEGJcP=;m8Vu!t%OTfX_xsT%v-fc`kSkbNx?I1Gsr;CTul4nrN}MDeEhgXJ>IJdEy?5%0MNx*xMpv0gY@S#WlE9W0`>6NLzN%P!%~vUaT}%qQH?H%}D+DTVxi8%#pCoSWXo&_K*(C5v0*5k%y%#4KROG~g>qNd$DoH>QxecyvUeF_MvV#F1A=F$@ky-dr@?fgitW+9WQvXgozv?i6H%^nPiheV9t-&AW;uY+qHE6>-b>f>v6`C|X1XF+BRui(T5pbqXlJ2>`gb-=+I4=?WDu%N81FJ;gwj!Wz{iAqo(J7b}aY{f#4CM^=e=EOHq+^w)t)MX8(0HSOZB>3u@K8n$w1pbs#qL^!sla!7}k!u7d6MDX(=x72V=3keJoB&BTtXOGtOOJR%zVRm0m+jEm(Hpd5L06OF5davt>M7w(l<;OTo8W~$Lc@Rk=OpPc*0wHZ=vZgNNXFm07H9NT?y2k=mMn#n+!>%ftX^d;a#0d-}P*yL#eX0<oC>p~^^YgC+C3qvnK&NtXe`AnfHL#=QWFm#AWi7fEju4$M=IV-*xU4W<sGy*f$5@#&<d3Dbebqc6>{{2Rkp?X@(v_lEQ}rHM%$0fR%-3?cVaunAE2f2p1u38r!${o?Q0_1Bd!1TC%vnnPISH9nJUk&ITqwIlK^XBn(WMJkqJ}8Zw%0w+aFzR8h_%r1@-@2OQQBLc=21&lD9j`jHV^O#1|K0Fgw#G;lHyBR^EKu{L=~RrM62(`**+NsqIInynOVzW4iSQa+r4)KcYi7d*JazPg1bsN5t(orfZ;kx{$PH0n>ce;t0D#^?m{Ox)2<RUs{A{NjP`u`EJAwfjlpEs<Wq7wOzJ(j`2&_bWBO7g=$94%QbjIkvpuGI`?m}ZG17Jl8k2C1GOmQ3P12*zsHySuPtsHu=G0kL9>s5no&wE7qaH*2v(8E6LZ!^bk+{4S8a2Wi=$NEbh0da2%3cz$mM}r7zmUP!Sf4&$h;&7qdqo>|$bG{6dlrj~=~f6InEf{&0noy{d9hl&D5CC-2&8Y;s=A3Qj#5$R>}(AnTKUatUE^MP6PhuQC31{RYfwH+*sV%QWv!95sQ7K*yI;1x`{L{Q?mSxo?bLyO`F?34wYCsd=&D}|{H!*N2vb(GSaYv$UCbOPhgg*v>Q<T96i3WsFEDqkJU&XbGQC7diqy!#=bM`PA$6{{B<q8O$5+oo`|?d@Voa(qclxo}>O-vW_^{B$-6b|X%SF;S1p~EJNZ2=<w>~WmkyBq7a?$msYWo#$4GcQG1r*LM>#$n?Ma>`yogT9W1YTg+qmwG|<mq(8f;I}d4nfseC|RKZ6pNHo&ua~LGI_Bb{kt#%{>Ge-8v}|v5Gs1;co%K7si8WZ44$3i=71<3Z$Sg5#;qRA1-@>*o}2F`V(GX+Ck<GlU6Hs=gVME+5X+QGn&oD@N+Kp7vcVQEOQY0_z$*rUr#ep?-e;A3`c8^*yK)YT{XL6g7~?;&)-}#=TKNyjz`QcjDSP?g(|N~6KpqvUc$AV)0v06;pkel%=;EcO%(cU@%uguE_o<X=7cu&qCxa(V18vkHOs!jAvFuf;;yrAImWeKr!wc>9^aVXjQ0rv@W?3wsDr9XhE*tuV;svPbJ8CR$w&G!Pto+)-vLSKcgdnLUvL+%1qFkcj`6;@R*&p$lPmY|yE!SAy$>BqJ0d;xGMalWr(mE3P;10qt>dA#v(8?BOB&JO&ZaAhN?G+$yO$n=FynY&3t#(I?^D{aufn3PhKTMH!*)KF97fw=AZFt5@eIZ`f(;uEoT<-s60dY!)-##GXNF23eHu!V^?%q%y{Z#r7H1YOZjm6h!^JAj&bthp=JU;WI^?><tg7kVZgDzI6AD>TKF&Otz=C>7_8YJe}8OsOme;Rr*GM%+3y&m#LH#WUy3juf**{<fMC`Ia}NW3c7h$@iDQ6YtB3|?@!a3oXXIKp$LG$B(O=!QK7v1H{xD+`F#gCtH>QewlAPEue1st8HkpGtsVGGpzSNI^4KL&c!QL0Qn9R8%dQToF5?uy8dLtVPK+O@(1P28@v{iS%m(`E-$icJN793$mecbbZ7)5t&jKc*_+V3)4s`S3|Vij>)}_{JquJbM64K`KwY40C`sC7?6u-1f_t+;dJrsPI5%WJA}8E{v{8}6*!!-!<hYDaIi7z-=Bv)Ug9pZQ^5f&2lCaLL2<VA?Nh;bP0i=XA;~%hm*m`nRj|O4H%vqABBNgN#<GQHfbQq>y!uxa>ic1nb%%=QmG(~Jyl=~rAUzLZszrp%xH(^rUQ+m4DsiVN#g&`vC5?-9EYN?T9PlxrPl6?=iU9$=g&`qBf}h4g&dxlMKca@O(BpcF4qms%n!%T$$r=G>Mi~a}R-F9jyo1+WbC!gDrFtyckvwMBuBw4~NqP{;YAar?HC0kvTVsG|`5fUYq<d?`0a6cYb7z79o|t;@g@ilxo3B!@FY9dcw2TbHiWY2?&aTyCg$!ff$5rn%Nu&|dy@-;LH~q>Qb1B=#>Ov2Htz#b%%>f{F&}urg-vEw9d<%$uJ03Q+T*U=W$$tHY5_Oi}j*dSmU?U2%3BccwtQ-r$F`~S*9%L~!N0wYT*Z+IJB>gE00BqD^27~1mtbCn9e!eU}NBh-TFCY_Zp#D~h;wFVr2i6flpCX8>w38*($mxlETdFs}ybL_D#w3Wht(9maQcuL<oJ0BhO6dZex|LYR`9w@VTfSYXzyU9|AmtFzQtB$Kb!{ZthzsIC-mYnxup{hcq?T2;bGT5Ckr_lV)j|$egvWQ5WZ*j+=e4Nw7qhXBg^j4dp-|M)R7U9N*Q!2^6!oA9LNqA_+LpDn4F&vZU30B|EJM8q%k=j+<?YE&^JF?oBn<DML#Cl!X)-QOJX3i`Xp~W?`kBG{Jtae`eHvQW<XhNEtT+ZOa>@IOVBu$lIQr1ancu!5nN}MKJ9xuNF1zs+bA$F*%(qce1KC8JJ+0EQE{20)8Lv%73ZVNbBNhP$prnu+9<bp!%iNz5J7#GtD@*#cPEpG`90r*4^Xt}Fn3al}@?0S!-B_Y%B3~gsfMG2#fK5;(VdcmZ(9QKO(B^E256;47wd+M$OAVDQvA34O#IggnP!N{$(=_}k?`u4t%Nlt=VpXbi5N>kGoxJK>hm;4VT7^!IpV$ks;Ap)Sbvw~#$heu#(M5+<%Cy%!MqiytIk%-ux#$Fs@E|(u)l;k|F><5uHPu=uzP}@!vpk23=-JR}ytK$|VY>pahUSiF366O=r9M2-O8+ZnOp=LV_uLTna*}bpw&_I2n~DyEUg2m<3r|?5<FH(EJh7FQu*W2Rk}XbCJElM-o4B@(!mvU$Xa*=G)v1?S^(n1}PTKAA(z_T$8M}BDp>s=C<mP*?Xfs$%2OE8QnVZz$8$cV&AcGWsGJHZq)0rV+lvy#P3~YB5-dt_nt8$yR({R;vn$-B*Okj;4dJSe4T*_<YcDhE<(&A!v0b56Zyt}pwQgbHMnaGvXXec!?89*1~;82q3k+oG(m0?&B139A<CylV`W1N@9MJ4$p>JFtYwC>?tRlsy7J&-mpQH1qdPrxCX6AN2GbLkjoM|II&)gU6KGAk_^ye&&m_p;v;qo_NFfOvjcA!2dyR3JNZEs1D5P}C9~V}%SUVBM<+ASG7>hika6Rp;u`g1j<~bWuT=@oI`GMRO_EJaH{aQbnJl`@j&UIyH(!urD?XTSClpEN$gXX&ja)$|BF*{8?jlU@$$rp(b=g47y1Pq@5|GI+!CVskx*yMH8YY1@M*F7g2zXF(X6TZcA<rp{{~a(MQ?h3eVH}Vvv~f1DjIHj8V;32wSa=rwMj|F_EMY5f>U)PfW?Hl$F4YdKo=+#ZZ!bxBiz?6s@C_wj!Pc7mJ_Cs=#M@HmR0=##D7%-(;Q04a*`ig(&30$X$f@jtXlgI=%9`D<q_`te|M$0u`n;FU|}`2Lcz0t0D{Auslb_QazUm3VLbb3W;q|;;_M^BB}Q**WhLm^Nv9IGMwBSBaw3B>6B#!pou(JWi~H`*(8aUT!)R(OZ54!94yvs0?z5uSkZDxPq2|4@uMNGYpW}EVH8y3)2$|CXW+)sn8gM(!F1E`7G>u(tCd%rMnkTAnk|WyrVf{(LP<&@LVZeqiFVa>sr-~sOeC*8UuUpJd$CW5%%opQRS$-!G+sNK%_|nId<a+iNtPqoiy?UD>7<=|mE?xveiu$1MMbh~n};iJOuKiNo&vu%?ld-{C<GSBzau2bT43)Vr~2A>;@E-4L{1$G(=boY980y<9U$$rB(h3%w{M#%b_C)3ufZBitDK`7h>G0Fv@nS#L3v@SjBvvHwxNYuUar3KDM5wmGL1<y9zZ3lU{^)rn@K5KD<dkDrL{c1)gU?<{VE+&m&kNEibNKmBbZ#6un-+Ich$!uOL#A-MwL`@-VbmvHkm6c<CpUDW!10xxn!BdI~AeQsW(OvXjS!%<1HHjMY9T%49*MHw9qK+EUYA>RJ1FlvP+<;LJZ+x=}fzB&TMihLPAl!;|d@t?5CZRPa4Z22-2O_Gs!BU4WK(*hmcyr?a#LZ1<bm(#(W=(P2)UK_N69)M^|Vl>i79Le0=B?-PdPY>3DL<wTql;1s2K_7rXc}lrm=zXqtfox6OBLxogw>(SWuXXK0q>+Y<Qlax63MQenm|z9$A8=;cLM`}>)3oNjjH>X-?+$>qcysU+snXmQ7@k@>Y)abrtlYWnPoFU(0zDTJt3gSXXFZcCoA1fn@CMkWSqBq`-|9<gv-vux#R5u6~wM`uhtR&<}?nhY`&bUNXIJ=j<U%Tn>4oPoz`Wr_?ul@`*YR3tf|PC?CZK6P5IQ}<#Fk;mArN>(9tB<)Yf0~S^WCX~=8Z4<>PuF_qrb0L65gkhHoTcTMD@)gH)^%_tsi{xfHmta<D5_ovP_F;X?l3;#DbBzK2<PkGb_ab#LU6E~%5~7hP`4til2o~Qf^u4SR>u7eiSkRO~c;h;FB{S}p6~>)fhJ-52QZKBxZflJv$(8C`gezX(6a3EBL9<qE8Mw`9c?qM7z?o{XtrLvM0s03XahV&Fe5GnIy}_V6DxX&AovL^v)}a7T>9#TsV92A_D!m2P-8Tzsp1drnFGjKvpfo(y*Iz+#PRBEPt25j@dFjBc9BEZ`F440xDRxR3Q?Yb_k}hR{Y!&h&DN~xQmNb^n1-v?ok;;~<B%Cdc9>HW<-_}&TXZ2oaeAsYGkq*3eQ);|QYvD29A|=f-08h*;&=Ud~>rv25I>NG}N|02kT$Oi7*O^(ZGXqmA1iO6Xq_UfwY{iw-L(ez01~1CVVjyNI@)OjeFlt>J0qsN^dD<6UaFkC@RwTj|TDL^k(B@0gdhsF~7txCv0z*QC_JpQHai$A8eQeOB7P9+Q5m|4ZRFsMvp{%88465~kLWIPE>5ydlc|bWaYA&RCDG~vVYH|7M_eT2}X>hGno!!E6Is358R$h81My?5~f$2A5B(|ep5p`@RPwYAZRw5CD@22c!OMW|1AxvLHO@X1?VyGu%jtQ6yGrM~0T5bwOE!Dzt1zy-;FyvU&Ffr$@Q%pT-lgjf-2q(QBVoTp*2ntIyR7)Yi&6ldUSX3=<9e@)?)oQQ6`&T782m$0kv%%lsSt%zStDU<b(V0G?R@PJl6^#XBqv=&#k~|DcV8OiPSDMI14r!4isn1)_a+McfqPwIBu$PLpmUQks5j0}1E2UgTeL{6UZz>Bl%t=xcV~QJ1)HbU|gxh7x)U|_3Q$ntjEeT_ttgUFm^F*Kp+fETUgW4aVJjRJD(5rX${HV)1m4_rJGNFHx+$C+=y5`TSYs*qdsNJhtB@;sW>8_0ZJi!Zjf;%xkc3iQ+0N4;hE1n%j8Io9<o4HPO!iZi{E?_cVEIG5cxaxVFb2gm5M;V9l4rhs-3K4wTu@DJbdOP3B@LZI}NQtnqzw!9Gu}EGWMLm(}bNaeLb_`}UV)rk*Vam|F*e<DPU4CZ?tuHr?+4PPq6qfusO^|?JCY2u+`C}CYx&o=8{g7sh0-78v(V|DR*@voNoJ^D}a9E1Wv=Sw+kFr-IN$4!KOxs;8sgMKBK$!*1F%OOEg5Ggy0fu)jdXAa2#!ztzGzy&>R;<A(DC<_x6STm7O+F?~OT0ChIB6zYnzW{5)3APAhqapYL(E{)sM@-jZ78A~$`Pd&SJ0vXHa}oh%GY6x%n9{@i0cUhQ4U>{ta0_EM>Mu|tj4E6-(ljP=0NjQ7|QyCK1JHl3zHkqpl2oNQiVLt^JWYAI670Aq@U@kwyJRxJVP(sTiyn6;<Q>4$_>`5D0N}xl=X?k*(sIY%u+J26HF;;|Emg_oWx4$eBC-(dRpbmlG5jMKq;bBkt5!}g8@f<6^m2F0VXmsqpJS2fcs%0VJEEEu74mH$CrAfb4l01Q4&Y-7~Kv^w!DmhU~sW45ioc09ingti|qoh%hM>$Nf|&oeGoQC!LCx_HJW*oA}!FV75ylNX<AA`mf{={&UMSiGGTqQre$A&3BD=7ffL9)F*FMc$t5UHiG9;6l{cjJV4HyI26cH(7rRmNaLvNNB=qz}2a-&*zFkfx(je<jNlOUFq9r9Vkd0b_ixTWgO+cE3Gi~{dqTtPmQ@9epK1<?Aa6M0gJl{u4r_`#J@+5Ny#Yna3`)hS;XmXl#aCsouwP8!aJbi*WCWG2aX<7{>?0X;yK~O|0oj0!%V>MALgrIBkIeRoWJFZibU~ru#%4bymCQ*!6@N~B>qXIz@8B0IYoC9(r&Jq=FqU25nJH`iTq4@$)3#<vkw`?j$!ZRg4`K?_+mQN;q;X#;)HxhCUYbkBx6x5h9NM5K*t>m()-o8$;(v}FgsVO;m%S^=2M+<r_u|1!`G(##Hw3Beu4Ap+N*Rn5DHL|b8k^wdBL*_(*HO&lCiYN#$(}kh4+O0cQWLyoYZ=gbRx_%mSglqY!ylSARWy1+H+J@5P9a8Kt!#|R+wNX276PI_+D+!C`<n(O1bgi-DX+wyb`5?8ci@MrWU94q$@RWjL!n>}6p6O6ksvxV>a#4E=DxFvj%KdY_SSa0qo(>(aJY$6sm|wsVdB+6iPQ6>5S8x+GUP-Oo4=c7}Bz{FL1@o;L*-6r6ylJfFvFm7K>=m)N>zMINB;2Ip#4#4{w-K|PFi9CvJ7#6zV2QX{#ktN&-aFjQiw-DBEs>%95A(lSP2;SZxME)6L;sYHZO@pwq&_zi+Q4q|H7)PAC1Uic9wjVJe)}P}t4;u+sD==qSJGmVvYP2_6&C(eUY?9KrIsd&_t~r2m6F7tG9GNM_(ScMOreoe;8TM$H%dhLPF*u19eQ}Ii|MLKg;M?9;DQS%uu5fAf!;;#D0asV?kyg2^4iLgLLSFQ*68fUxe0-$WMIsAfQ0fU^2&+>+rCMv1J~PAqKQdL>vZ)LgrgGaRKG$h=qWw?lrlo6?W<1G>+fsaO7hw_j}Pw;-}>^+<OA<3_}TMUEY;j#+Y8!D?XGJ(vHP(5@$4Hy$6M*GJqRLh&EluOKm8xH6Mn$')).decode("utf-8"))
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


def _clip_seed_surplus(action, obs, step):
    """Remove only opening or carrot seed orders the route cannot consume."""
    step = min(max(0, int(step)), len(_ACTIONS) - 1)
    if step == 0:
        demand = {}
        for future in range(step, min(len(_ACTIONS), 24)):
            trace = _ACTIONS[future] or {}
            for order in [
                trace.get("farmer") or ["PASS"],
                *list(trace.get("hands") or []),
            ]:
                if len(order) >= 2 and order[0] == "PLANT":
                    demand[order[1]] = demand.get(order[1], 0) + 1
        seeds = _get(_get(obs, "private", {}) or {}, "seeds", {}) or {}
        action = _copy_action(action)
        market = []
        remaining = {
            crop: max(
                0,
                int(quantity)
                - max(0, int(_get(seeds, crop, 0) or 0)),
            )
            for crop, quantity in demand.items()
        }
        for order in action.get("market") or []:
            if len(order) < 3 or order[0] != "BUY_SEED":
                market.append(order)
                continue
            crop = order[1]
            required = remaining.get(crop, max(0, int(order[2] or 0)))
            order[2] = min(max(0, int(order[2] or 0)), required)
            remaining[crop] = max(0, required - order[2])
            if order[2] > 0:
                market.append(order)
        action["market"] = market
        return action
    crops = {
        order[1]
        for order in (action.get("market") or [])
        if len(order) >= 3
        and order[0] == "BUY_SEED"
        and order[1] == "CARROT"
    }
    if not crops:
        return action
    required_now = {}
    seeds = _get(_get(obs, "private", {}) or {}, "seeds", {}) or {}
    for crop in crops:
        stock = max(0, int(_get(seeds, crop, 0) or 0))
        current_trace = _ACTIONS[step] or {}
        current_plants = sum(
            len(order) >= 2
            and order[0] == "PLANT"
            and order[1] == crop
            for order in [
                current_trace.get("farmer") or ["PASS"],
                *list(current_trace.get("hands") or []),
            ]
        )
        current_orders = sum(
            max(0, int(order[2] or 0))
            for order in (action.get("market") or [])
            if len(order) >= 3 and order[:2] == ["BUY_SEED", crop]
        )
        # PLANT is atomic per crop and resolves before the market.  If the
        # current request is under-stocked, every current PLANT of that crop
        # fails and the existing stock remains available for later turns.
        balance = stock - current_plants if stock >= current_plants else stock
        deficit = 0
        for future in range(step + 1, len(_ACTIONS)):
            trace = _ACTIONS[future] or {}
            unit_actions = [
                trace.get("farmer") or ["PASS"],
                *list(trace.get("hands") or []),
            ]
            plants = sum(
                len(order) >= 2
                and order[0] == "PLANT"
                and order[1] == crop
                for order in unit_actions
            )
            balance -= plants
            deficit = max(deficit, -balance)
            balance += sum(
                max(0, int(order[2] or 0))
                for order in (trace.get("market") or [])
                if len(order) >= 3 and order[:2] == ["BUY_SEED", crop]
            )
        required_now[crop] = min(current_orders, max(0, deficit))
    action = _copy_action(action)
    market = []
    remaining = dict(required_now)
    for order in action.get("market") or []:
        if len(order) < 3 or order[0] != "BUY_SEED":
            market.append(order)
            continue
        item = order[1]
        required = remaining.get(item, max(0, int(order[2] or 0)))
        order[2] = min(max(0, int(order[2] or 0)), required)
        remaining[item] = max(0, required - order[2])
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
        game = {
            "last_step": step,
            "active": {},
            "post_recovery_market_regime": False,
        }
        _WEED_STATE[seat] = game
    game["last_step"] = step
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    active = game.setdefault("active", {})
    # The engine resets all workers to the shed at each day boundary.  A
    # delayed route replay is position-dependent, so carrying it into hour 0
    # would execute yesterday's movements from the wrong location.
    if step > 0 and int(_get(obs, "hour", step % 24) or 0) == 0:
        active.clear()

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else int(actor) + 1
        if index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[index] = list(transaction["intended"])
        elif 2 <= age <= 1 + _WEED_REPLAY_STEPS:
            delayed = _trace_actor_action(step - 1, actor)
            unit_actions[index] = delayed
            if delayed and delayed[0] in ("NORTH", "SOUTH", "WEST", "EAST"):
                # Rejoin early only when the first delayed move reaches an
                # in-bounds visible empty tile. Movement has no unit collision
                # rule, so the move is executable; the current raw-route
                # action is deliberately discarded to regain the timetable.
                # An occupied destination can still need the next delayed
                # WATER/CARE action, so its bounded replay is preserved.
                if not transaction.get("first_move_seen", False):
                    transaction["first_move_seen"] = True
                    try:
                        x, y = int(positions[index][0]), int(positions[index][1])
                        dx, dy = {
                            "NORTH": (0, -1),
                            "SOUTH": (0, 1),
                            "WEST": (-1, 0),
                            "EAST": (1, 0),
                        }[delayed[0]]
                        destination = _tile_at(farm, (x + dx, y + dy))
                    except (IndexError, KeyError, TypeError, ValueError):
                        destination = "LOCKED"
                    if destination is None:
                        game["post_recovery_market_regime"] = True
                        active.pop(actor, None)
                    else:
                        transaction["preserve_bounded_replay"] = True
                elif not transaction.get("preserve_bounded_replay", False):
                    game["post_recovery_market_regime"] = True
                    active.pop(actor, None)
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


_PASSIVE_WEED_NOOPS = {"PASS"}


def _clear_passive_weeds(obs, action):
    """Turn only otherwise-certain tile no-ops on visible weeds into DIG."""
    action = _align_hands(action, obs)
    farm = _farm(obs, _seat(obs))
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]
    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        if not isinstance(intended, list) or not intended:
            continue
        tile = _tile_at(farm, position)
        if (
            isinstance(tile, dict)
            and tile.get("kind") == "WEED"
            and intended[0] in _PASSIVE_WEED_NOOPS
        ):
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
            market.insert(0, ["SELL", item, quantity])
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
_COUNTER_META_SALES = {148: {'WOOL': 6}, 151: {'WOOL': 6}, 197: {'MILK': 12}, 222: {'WOOL': 4}, 223: {'WOOL': 4}, 256: {'MELON': 12}, 257: {'MELON': 12}, 258: {'MELON': 6}, 259: {'MELON': 12}, 260: {'MELON': 12}, 262: {'MELON': 12}, 264: {'MELON': 6, 'MILK': 6}, 288: {'MILK': 6}, 312: {'WOOL': 7, 'MILK': 6}, 318: {'WOOL': 1}, 336: {'MILK': 9}, 344: {'WOOL': 6}, 360: {'MILK': 6}, 366: {'MILK': 12}, 372: {'WOOL': 6}, 384: {'MILK': 6, 'STRAWBERRY': 8}, 408: {'MILK': 6, 'STRAWBERRY': 4}, 416: {'WOOL': 10}, 417: {'WOOL': 2}, 422: {'WOOL': 1}, 427: {'STRAWBERRY': 6}, 432: {'MILK': 24, 'STRAWBERRY': 6}, 455: {'STRAWBERRY': 10}, 456: {'STRAWBERRY': 14, 'MILK': 6}, 463: {'WOOL': 12}, 464: {'WOOL': 22}, 480: {'MILK': 30, 'STRAWBERRY': 12}, 501: {'STRAWBERRY': 8}, 504: {'STRAWBERRY': 18, 'MILK': 6}, 514: {'WOOL': 1}, 516: {'WOOL': 5}, 517: {'WOOL': 2}, 518: {'WOOL': 3}, 521: {'STRAWBERRY': 6}, 524: {'STRAWBERRY': 6}, 525: {'STRAWBERRY': 8}, 528: {'MILK': 24, 'STRAWBERRY': 18}, 545: {'WOOL': 2}, 551: {'STRAWBERRY': 8}, 552: {'STRAWBERRY': 15, 'MILK': 6}, 553: {'STRAWBERRY': 3}, 562: {'WOOL': 8}, 564: {'WOOL': 4}, 566: {'WOOL': 5}, 569: {'STRAWBERRY': 2}, 570: {'STRAWBERRY': 6}, 572: {'STRAWBERRY': 2}, 573: {'STRAWBERRY': 7}, 575: {'STRAWBERRY': 1}, 576: {'MILK': 24}, 578: {'STRAWBERRY': 17}, 591: {'WOOL': 4}, 596: {'STRAWBERRY': 3}, 599: {'STRAWBERRY': 8}, 600: {'STRAWBERRY': 17}, 601: {'MILK': 6}, 602: {'STRAWBERRY': 10}, 608: {'WOOL': 4}, 611: {'WOOL': 4}, 612: {'WOOL': 2}, 614: {'WOOL': 3}, 616: {'MILK': 5}, 618: {'MILK': 1}, 620: {'STRAWBERRY': 3}, 621: {'STRAWBERRY': 7}, 625: {'MILK': 17}, 640: {'MILK': 1}, 644: {'STRAWBERRY': 2}, 645: {'STRAWBERRY': 3}, 646: {'MILK': 1, 'STRAWBERRY': 1}, 647: {'STRAWBERRY': 9}, 648: {'MILK': 5}, 649: {'STRAWBERRY': 13, 'MILK': 1}, 653: {'WOOL': 8}, 654: {'WOOL': 5}, 656: {'WOOL': 8}, 658: {'WOOL': 2}, 665: {'STRAWBERRY': 6}, 669: {'STRAWBERRY': 10}, 672: {'MILK': 24, 'WOOL': 8, 'STRAWBERRY': 13}, 696: {'WOOL': 4, 'MILK': 6}, 717: {'MILK': 18, 'STRAWBERRY': 2}, 718: {'WOOL': 4, 'STRAWBERRY': 2, 'MILK': 6}}
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
    # A fast weed rejoin marks the remainder of this episode for a wider,
    # inventory-backed sale scan. This is deliberate opportunistic
    # liquidation, not an H1/H7 prepayment and therefore has no repayment
    # ledger at a later route step.
    market_scan_horizon = (
        11
        if _WEED_STATE[_seat(obs)].get(
            "post_recovery_market_regime", False
        )
        else _META_HORIZON
    )
    if int(state.get("clone_confidence", 0)) < 1 or market_scan_horizon <= 0:
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
    end = min(len(_ACTIONS), step + market_scan_horizon + 1)
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
            + (market_scan_horizon + 1 - distance) * _META_BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        action["market"] = [*orders, ["SELL", item, quantity]][:10]



_COUNTER_DECISION_STEP = 72
_ROUTE_DECISION_STEP = 168
_ROUTE_STATE = {
    0: {
        "last_step": -1,
        "shops": (),
        "counter": None,
        "expert": None,
    },
    1: {
        "last_step": -1,
        "shops": (),
        "counter": None,
        "expert": None,
    },
}
_ACTION_CACHE = {
    0: {"step": -1, "signature": None, "action": None},
    1: {"step": -1, "signature": None, "action": None},
}


def _action_cache_signature(obs):
    """Serialize decision state while ignoring retry-budget bookkeeping."""
    try:
        payload = {
            str(key): value
            for key, value in obs.items()
            if str(key) != "remainingOverageTime"
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
    except (AttributeError, TypeError, ValueError):
        return None


def _counter_public_signature(obs):
    """Match the repeated public 2C/2S route on its validated shop prefixes."""
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return False
    shops = tuple(
        str(value)
        for value in (
            _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
        )
    )
    if not shops or shops[0] not in {"BAKERY", "PIZZA_SHOP"}:
        return False
    opponent = farms[1 - _seat(obs)]
    counts = Counter()
    for row in _get(opponent, "tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value:
                    counts[str(value)] += 1
    try:
        money = float(_get(opponent, "money", -1) or 0)
    except (TypeError, ValueError):
        return False
    return (
        money == 49
        and len(_get(opponent, "hands", []) or []) == 0
        and counts["COW"] == 2
        and counts["SHEEP"] == 2
        and counts["MELON"] == 12
        and counts["WHEAT"] == 7
        and counts["PASTURE"] == 5
    )


def _select_route(obs, step):
    """Select routes from public shop demand and opponent farm behavior."""
    seat = _seat(obs)
    state = _ROUTE_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {
            "last_step": step,
            "shops": (),
            "counter": None,
            "expert": None,
        }
        _ROUTE_STATE[seat] = state
    state["last_step"] = step
    if step <= _ROUTE_DECISION_STEP:
        town = _get(obs, "town", {}) or {}
        state["shops"] = tuple(
            str(value)
            for value in (_get(town, "unlocked_shops", []) or [])
        )
        if (
            state.get("counter")
            and len(state["shops"]) >= 2
            and state["shops"][0] == state["shops"][1]
        ):
            state["counter"] = False
    if (
        state.get("counter") is None
        and step >= _COUNTER_DECISION_STEP
    ):
        state["counter"] = _counter_public_signature(obs)
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
    if state.get("counter"):
        return _COUNTER_ACTIONS, _COUNTER_META_SALES
    return _LOW_ACTIONS, _LOW_META_SALES


def _v5_is_shed_access(position, board_size):
    """Match the engine's four orthogonally adjacent shed-access cells."""
    try:
        x, y = int(position[0]), int(position[1])
    except (IndexError, TypeError, ValueError):
        return False
    half = max(2, int(board_size)) // 2
    return (x, y) in {
        (half - 1, half - 1),
        (half, half - 1),
        (half - 1, half),
        (half, half),
    }


def _v5_projected_shed(obs, action):
    """Project same-turn shed stock in actor execution order.

    Kaggriculture resolves farmer and hand actions before market orders.  SELL
    ranking therefore needs the stock after executable DROP, PLACE, and PICKUP
    actions, not merely the stock visible in the observation.
    """
    farm = _farm(obs, _seat(obs))
    private = _get(obs, "private", {}) or {}
    projected = {
        str(item): max(0, int(quantity or 0))
        for item, quantity in dict(_get(private, "shed", {}) or {}).items()
    }
    inventories = list(_get(private, "inventories", []) or [])
    positions = [
        _get(farm, "farmer", [0, 0]),
        *list(_get(farm, "hands", []) or []),
    ]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]
    tiles = list(_get(farm, "tiles", []) or [])
    board_size = len(tiles) or 10

    for index, unit_action in enumerate(unit_actions):
        if (
            index >= len(positions)
            or index >= len(inventories)
            or not isinstance(unit_action, (list, tuple))
            or not unit_action
            or not _v5_is_shed_access(positions[index], board_size)
        ):
            continue
        inventory = {
            str(item): max(0, int(quantity or 0))
            for item, quantity in dict(inventories[index] or {}).items()
        }
        operation = unit_action[0]
        if operation == "PICKUP" and len(unit_action) >= 2:
            item = str(unit_action[1])
            try:
                requested = (
                    max(0, int(unit_action[2]))
                    if len(unit_action) >= 3
                    else 1
                )
            except (TypeError, ValueError):
                requested = 0
            quantity = min(requested, projected.get(item, 0))
            projected[item] = max(0, projected.get(item, 0) - quantity)
            continue
        if operation == "DROP":
            deposits = list(inventory.items())
        elif operation == "PLACE" and len(unit_action) >= 2:
            item = str(unit_action[1])
            try:
                x, y = int(positions[index][0]), int(positions[index][1])
                tile = tiles[y][x]
            except (IndexError, TypeError, ValueError):
                tile = None
            structure = {
                "COW": "PASTURE",
                "SHEEP": "PASTURE",
                "GOOSE": "COOP",
            }.get(item)
            if (
                structure
                and isinstance(tile, dict)
                and tile.get("kind") == structure
                and "animal" not in tile
            ):
                # Matching animal placement never falls through to the shed,
                # even when the actor does not carry the requested animal.
                continue
            try:
                requested = (
                    max(0, int(unit_action[2]))
                    if len(unit_action) >= 3
                    else 1
                )
            except (TypeError, ValueError):
                requested = 0
            deposits = ((item, min(requested, inventory.get(item, 0))),)
        else:
            continue
        for item, requested in deposits:
            room = max(0, 100 - sum(projected.values()))
            quantity = min(max(0, int(requested or 0)), room)
            if quantity > 0:
                projected[item] = projected.get(item, 0) + quantity
    return projected


def _v5_prune_terminal_wheat_seed(action, step):
    """Remove WHEAT seed purchases after the route's last future planting."""
    if any(
        len(unit_order) >= 2
        and unit_order[:2] == ["PLANT", "WHEAT"]
        for future in range(int(step) + 1, len(_ACTIONS))
        for unit_order in [
            (_ACTIONS[future] or {}).get("farmer") or ["PASS"],
            *list((_ACTIONS[future] or {}).get("hands") or []),
        ]
    ):
        return action
    action = _copy_action(action)
    action["market"] = [
        list(order)
        for order in (action.get("market") or [])
        if not (
            len(order) >= 2
            and order[:2] == ["BUY_SEED", "WHEAT"]
        )
    ][:10]
    return action


def _v5_market_finalize(action, obs):
    """Rank sell slots by executable local impact, then merge duplicates."""
    action = _copy_action(action)
    orders = [list(order) for order in (action.get("market") or [])]
    params = {
        "WHEAT": (25, 10000, 400, "sqrt", 0.8, "log", 0.2),
        "CARROT": (35, 10000, 450, "log", 0.2, "sqrt", 0.7),
        "TOMATO": (60, 10000, 200, "linear", 0.4, "sqrt", 0.6),
        "STRAWBERRY": (120, 10000, 100, "sqrt", 0.7, "linear", 1.6),
        "MELON": (250, 10000, 300, "log", 0.2, "sq", 3.6),
        "EGG": (50, 10000, 332, "linear", 0.4, "log", 0.2),
        "MILK": (160, 10000, 122, "sqrt", 0.6, "linear", 1.6),
        "WOOL": (200, 10000, 105, "log", 0.2, "sq", 3.2),
        "FERTILIZER": (100, 10000, 200, "linear", 0.4, "linear", 0.4),
    }
    inventory = _get(_get(obs, "market", {}) or {}, "inventory", {}) or {}

    def shape(name, value):
        value = max(0.0, float(value))
        if name == "linear":
            return value
        if name == "sq":
            return value * value
        if name == "sqrt":
            return math.sqrt(value)
        return math.log1p(value) if name == "log" else math.log10(1.0 + value)

    def price(item, market_inventory):
        (
            base,
            equilibrium,
            scale,
            below_func,
            below_target,
            above_func,
            above_target,
        ) = params[item]
        if market_inventory < equilibrium:
            value = (
                base
                + below_target
                * base
                / shape(below_func, scale)
                * shape(below_func, equilibrium - market_inventory)
            )
        else:
            value = (
                base
                - above_target
                * base
                / shape(above_func, scale)
                * shape(above_func, market_inventory - equilibrium)
            )
        return max(1, int(round(value)))

    def score(order):
        if not (
            len(order) >= 3
            and order[0] == "SELL"
            and order[1] in params
        ):
            return float("-inf")
        item = order[1]
        quantity = max(0, int(order[2] or 0))
        start = int(_get(inventory, item, 10000) or 0)

        def revenue(market_inventory):
            total = 0
            for _ in range(quantity):
                quote = price(item, market_inventory)
                total += quote
                if quote > 1:
                    market_inventory += 1
            return total, market_inventory

        now, delayed = revenue(start)
        later, _ = revenue(delayed)
        return max(0, now - later)

    projected = _v5_projected_shed(obs, action)
    remaining = dict(projected)
    sell_rows = []
    for index, order in enumerate(orders):
        if not (
            len(order) >= 3
            and order[0] == "SELL"
            and order[1] in params
        ):
            continue
        item = order[1]
        requested = max(0, int(order[2] or 0))
        executable = min(requested, max(0, int(remaining.get(item, 0) or 0)))
        remaining[item] = max(0, int(remaining.get(item, 0) or 0) - executable)
        scored = list(order)
        scored[2] = executable
        sell_rows.append((score(scored), -index, order))
    sell_rows.sort(reverse=True)
    ranked = iter(row[2] for row in sell_rows)
    orders = [
        next(ranked)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in params
        else order
        for order in orders
    ]
    premium = {"MELON", "STRAWBERRY", "MILK", "WOOL"}
    for index in range(1, len(orders)):
        if not (
            len(orders[index]) >= 2
            and orders[index][0] == "SELL"
            and orders[index][1] in premium
        ):
            continue
        cursor = index
        while cursor > 0 and (
            not orders[cursor - 1] or orders[cursor - 1][0] != "SELL"
        ):
            orders[cursor - 1], orders[cursor] = (
                orders[cursor],
                orders[cursor - 1],
            )
            cursor -= 1
    first = {}
    merged = []
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            item = order[1]
            if item in first:
                merged[first[item]][2] += max(0, int(order[2] or 0))
                continue
            first[item] = len(merged)
        merged.append(order)
    action["market"] = merged[:10]
    return action


def agent(obs, config=None):
    """Return the V5 action for one Kaggriculture observation."""
    try:
        global _ACTIONS, _META_SALES
        raw_step = max(0, int(_get(obs, "step", 0) or 0))
        seat = _seat(obs)
        signature = _action_cache_signature(obs)
        cached = _ACTION_CACHE[seat]
        if (
            raw_step > 0
            and signature is not None
            and int(cached.get("step", -1)) == raw_step
            and cached.get("signature") == signature
            and cached.get("action") is not None
        ):
            return copy.deepcopy(cached["action"])
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

        action = _clip_seed_surplus(
            _copy_action(_ACTIONS[step]), obs, step
        )
        action = _weed_repair_action(
            obs,
            action,
            step,
        )
        action = _clear_passive_weeds(obs, action)
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
        action = _v5_prune_terminal_wheat_seed(action, step)
        action = _v5_market_finalize(action, obs)
        _meta_remember_market(obs, step, action, meta)
        if signature is not None:
            _ACTION_CACHE[seat] = {
                "step": raw_step,
                "signature": signature,
                "action": copy.deepcopy(action),
            }
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
