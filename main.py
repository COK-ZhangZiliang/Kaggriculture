"""Kaggriculture V3B: adaptive 8C/4S production and market counter.

The field route is a majority reconstruction of public episodes 92165990,
92185587, and 92223213 from submission 55440039.  The controller adds
bounded weed/cow-placement recovery, a quantity-conserving one-turn lead,
and an evidence-gated second-order counter derived from the public Breaking
the Tie premium-sale schedule.  See THIRD_PARTY_NOTICES.md for provenance.
"""
import base64
import copy
import json
import zlib


_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-qxnO>Z075&SPY&%ylAhjY`~Ojd~2GGsYKVi1c3k|02k95%TH`R~zM<d8F6U0vPp(b}ArE0Z(t`*l}WSAY4>#b1B=`5%Az`QkTUE<WCV`gE}yF8=n@KmYu%=RZ7u{Kro}|NSrje*XOB;=9j({PE-C!~4(go-T%q?f0A8=l?F&yWz{l_jiw*i{QgAKfnEO_rvY|^RM4MY@dH?{`~3t&F169us;05r_JX5^Phj%+&_G{7%pdj-Z$a$_?q2+he?0#-u?db$CKBMJ^OO8-F$lb+OF}#yW4$B$Df@x=VffBBl2l;e}8PpTioguZuQb_>|tal&HeE3`1JkP)*V0Xr_27-Y4GfY`;MzG`R?=G{rexE|M%(hVVt5j%zq;H=l=HH<~aTf>1Br>fw_MErw>o#j7(oT&iZeEnI7p)`){5urrW2@qxazBx{4mW|0W!!LmytIc=Fu&2(m$%?QrzmV`p0C-uC7AT(IRzGj2LFKA4P_KF_ubpB_H%M;Z)L%RJi^dhE*K`AyS&(q1z(ou_#`SjSiPo@QmVTBcbVEPc9d2gcumF`9KHw~P*rJ1$iBPq`64Ihtof-?DmgBhzd392&g2tuGqVayvv_t^zhP_2*6v8fZm%%d9Zy=l;n{Q(wJd-l52T@^F8@dH3|=Z#R!mclURH`Z~kb5J;JG;b?$G2AV-0aJZ6E4fU3G!{{WNeK-nxPSF0Dsf85(rZQIf?b_un-=<;b_z8D=_fFo)yq|iUa}U=z$k#jlWN*5dyZ+Ym_T6qSa_;PC<iy8?^|qk93m)V&^=g-JyM*H`I2cBoqJD%QFa6wE44bAj#6Q=oO&LcaJZKN*O>Gpw5aL0ov}5ktNINEM;E7XNXwz|ED`PWtI!gTk)8&kK*g)oR7tXg97qH2@!~JhLq0@$K%N;faDi^aqe|mbn-F~-ueEj1t*yih9P$^$!pkpcDX;BNMZfY0f>_fK;a;TZ;2(RsbH@4oA2iN;#jpl5F#jfNc4FCeJyp7+x<n{?$eLM^C5H<Th0G<e+3H&g6TQ^-)Q3nimoE;%Bc?d5CPG7_F06Qr5DrrmIkVDnrJFbV=Lb1lgc(Bfb2B`z$_>dWPR<uKB$YBj9>;>BCmpc!VN{$-Yf@)N@dSA6h&}t7X-(bYAo*P(cH&A*@#TSW=-^9qV@Ul4*Y7d+_mA@>w+s8l1@e|}R+ky5%KwVsM5G<=a9Xv)4BY}f%?vmyjxIZ2FF8OuLl<vKrwl^^r$Dd)Z)<)kq^{d6da~qxD@xDvVnru6RiOWwVan3pohv!PR#tVg~HMlF8*PO}jaL|J_p@ntebJbmixjnMXSStm89oY`CL+1N<v8~qbF8L-&KXle{#(EhYHRhT%I>M<U)U?tt+7+Y@W9-UFgr0Z+tqpLz^v2ud<wI?a&mY$Vx^O)IPI2_y_2Wj1PY1BjvIqz&M}7nEx_*Nd5CGOj`60xhI8KG!(PieUR;Q+eS&%?Pz9|f`%EJ(f=?z}<O)l^HOr4tCSr8@>ua|)ihVM2250=afar7zWesR4kUyX_TmZ3@sCPOsD*u|{Gb*+t3GAaP1UkE*jn3B7eX~0oN^?MmF3A@8S2G4N#p!bgtADsy%w$yR6JUra*(^J49J?5u8Upnv2v26QbK>_q?>((trw{Dr+y}B{Uy}I!^<BHLrOuU8TV+~9-yWM9Gsksv%{Uou@*yW~7d*awEglsF;$jj1yz9z&ZwN(Dv(!E`mMMUB2V^_er91=kiZ#$Y+t_e2t7L!3%dY4<mJT@d%W*{giN%GTK;S}`V$Y*P0PlyK6z$}8)=&W?JlpRUHDRBB?5BDUlWS5c6b|GUjU@8El5yC4vxtiuT1UgSNMu>9GGy4;a30*|Vd0~Me5X6#~M+?EzhLm{VGbEnq7r31XuuP481D9rTqX0?|Sd7+svj%M=Z^Q)(1>=L+`06qshBJ#;hKF%^tJouKX363ChoN=B4b;+QfZ;MoWTfKdPhX4TC;dj-ZUfMSagDsc`yFmdtF1#aqun7MT2hrNw?Na|ln*AKwLGn<*CrAf(qQX#z~f%k{F@wVn~IbkS#(gpVvY*r>~G(-5j+*@Be)*fvU(~}<Nx&B9Y;*SMwhz|NtBU8lJPv0q$2EXSR+PX373i4)*TAhrb(0ilE)^PgK>d$PN0Rh;`mnY)@TmS+q-aXo-{(?C&4@1>r6tHLe&HosOvp;B~LhZ)NJJ{>jxOvz-T<aZya^wWyZ^dq3_m?ficqDRm)xoO_%7PtRz0z?M!hCBiB>RZgZJ;9vW~Q2Dol86};1F<XegpYodYcV$U3e;7F4&zmKnW74Z}MDuAuD@F7@8%I>FLtIW%!sPQtGG|E19MtdTHZdr?b@uoHG&_YRNPER&Rk(>2PY$|Z8zM7gyZurQ0u0;??T%4N5B^z0eo}*XW8Sj~^3GVyQOjZwac5Ytp3N{{UV~MjNu_7QnUQ2-MpNDFPz}oCOw%@iY#swLzgHq0-pBkHi`r}uNh(0wL+W0)+CBP0F&`zi$*v#e!W*1mxErAPU;vwa;$c2lyI55W1^oDMuJ2**^5rDzlKgpTJ`@{5yyZhe@HVwK&5cdgsD@~q=wNg$W%^a3;vP>!`=eWG1v#f<!teA1SNv<RxM?0ynb|IPW4*g>kpqnYp?c9dB(owJLNaqA|_ZC+r8q-vu`nnUkzjT7`x*uSJjv!dTzSKnIp2-DiZwMMo$tq3BUI6GaMgWL`Zv|&a{91pw*-O$GIIDx><c(dimWjnis(z5|FAMgFU9S1g)Tad&y#>Qg#F(}DV8JZi3j^}lcKxH(!@W0Z;Ol<ey6nfH#U<DTP@$a2->bN8Sxg5guhjMkNWMayr4u(BiHbz*;9;j`S!<I+xi<-?aX!f~nn5(G(Wu%UjA$xwM4a@MO`M>xH$-0WQYUJELpY;OwGcsE$f}t~96Ud=HT#M4XBsvm!uByIO`$q4KRZVMhv4hfJ4O8!M3enx?G8;Ik7NPU@gK*v4;+2krTIF)@|W@@*#TEQ7c@h1atoT8kJ+IrEmwR5@ij<|8?Z-bCm=n>EYP5w&0rDQv&K?3VMhXhO7r=XI&JF8W7ms43Egv;+N6b$7rOAlx)~1v;Lb-)CYS)I*P+BK#{)%QaBQ?}yCD4O;}`6iO@e#gk>rC%;Zh<-G@E3<4A}g14~SnHLEP^kE8L`jPRc?n6b~6XeK-^GR#}(lK*RjxHUSQ^23A%GV4Yw=qDEISqDE{BHHD#Dtu3j+R-s|!Z(it<yE#HNnCcAi`fe}|LMXM+y`Lx4UGO=$gkb#Dc!v~xNsM7LcaD&;sLUu_1cg|(n{1a}mOM&pVZAE5AoS!3VoNnWa_s3O3xUIAM0k?JoG1#ljBOi+5!g*baqbM_Z5wi8%I{OGn9)kdH78ZGNDNZ!I;A!WI4etOmTWY&I|5?u72*WtY)j|^W2b7=s-#9Q!*@x@f|ZD@@Jlq6vFrzP#?+KmnX^pGs_@noq)Pg_7v0z~I=%NB3`Bvg(joWp|H!?h4NnQ+Va_#(a3Os=(YqYKc6zxl-G5o=?&pmz_yJY>0GFBqpp=x^QdvjN)bxm$#g;Vj!r7g2W{(+lS|)L-1do=iKs<X1hr=4S<B!B32VC(|DiD}r>K12gJy}Q*dpMB1NjO{yIyO-#wnGHy$y(AUjmY<4Mo>`%Ns)s~e&K|qIKW1QKf=MI8$PpV?fOHdD10v#q+d|hOVhf;djR+vFu)8q4RgL<$lO=W6|TTG5hfcAsF!@{SO|eqfpzXU3<XX<HXE5^kcS1~7GZ3k6FT|nC80ZXsAO7$u8=iT1g1w){t5B<8P|jzhq-hEyN-<R3qV2jM33=l)7h--0gIt&HE%3C#T6;nwRTM7GHp{xyi%kxo?okrn`%Xu91Bf`bbrvTf7Nd5d19a~iNT3@ClDmn;_x{=81>Wnqn@%rDb5?|9ac)EA*VRh0*R3Y$a7FRBeB*Zn=1Qk>r&4<SC=57J}j*-Rl0Q9ukb+ZuMx~x3~Fg(N&+@$%QkaRD>5=c?lFm;XApcbWtPTY+@Ms|8V3(d5GZqRwT~g3>B>8KVz4es6q&F9|EkVA(v$TWOtZiA910lu-grw<(yMMtn})b>Ru8%%f&0Ww@$;c<QcGVU?_4f&L{N@$g&HKF!sr?QOXo13^2&lV6XAtgN7DX<v0%Th)AjD$A-$F^D)jJj;i_dOZr3GA+K<~cRs8TD3ry7@`KwT!LOANYQjDBa^jei2Y$G+|UEmJ@_wH?bq3=jCUoRBS%)5HMFfq=M{MXb@IVG@xh~J=wtrPYy+X5_{M8kvqVq12p$BZ?S*IzN!B&gEE!Y7ct9iR+5IuT;f>bbLoJ(_@7Ft7RkQB2tOAwX>a)+&>@(CHQFnjN8_19eLZY<?z$5^gfcxjkL%4cA}VJHz_6jXYmc+=5A!p%O9X3~PEj3v{_kt_}0Eiv2EHgCSbjpoYqfyIC72g4l%sU>9X9Fe=A4SP@xDR3!<UU%jJ6#*GKu*n(VG53Q0{rD3v6$jH-E3r0*7!)_+c<tR*ryJ;=u0(X;DrI>OxDUoE5at1jyvxl-&!C$3OGsiz|6t~J(dsjK4RJT|vc7b)`*1NK-t0E`M<<TnEpLBng(!v@{9dZ3<3I#x`D46@omay}Q#jYr!ZnQ{xYz`t|Is|TQD%V8i#IeLdPxFanGv!207$-C$t`ag|2H#+US0u<q1Btod62l^qB8ytGMyMuNt^LlZrI9L4s<K<Kis?X!!PoQPbo?+r9huR_<^@pV7}-J~Lr`4hn7d64H|pHxvM4v<Y^VrOOPQUNT4PM;q}u*_6T6~`0>pSE8f)kj61u1Y;x{>@lEAABNy3{e?-4GF9wD$mm#?6&oJq!OkWntg!dpUyeUxONm$-8OC6s4|zq-Vmf2vS8NF}4BI^ceqqJC&8nmc{shC(=#F!TgJ`WxstGY>Eu-J~i<T-t@BGjjAZp{19pzT$+H*lnvhTg==#r49oqIW8q4N?#=We5uYVaD1Ra$g&|-dRR*~JS*O;Wn-ea7Iqax*SnR%9jd1?4R*F?nN(e=91a38P%KBs<-GmM0_L)xv{Zs-VTH#bC|@qh#PcJn6}N!+CO%fUA5H1Y!lIE1>yRuk5F>;bvUj}Wr5R_LGU=qIKs1lFZiHi1TP6U_#X|_L6+M1Uc{Cyk0UD$?yG(!BW(@+}xU3R9dlVfPDc6a~0R?+F5Gux-z^m@r04LkxEON4Il%-9T>6CEyISPK;{vxLU^UoO3upvK<qYH?ZV!q_H*i}Xj_w8bR8o~7n50`4xS|W5C5l9PDPkfq}%u!)=k=kN0Wg#mx)jeJI8}q=E1-K^Q4`vYbXNb3C&B|2qVrFA9;_o^OA))!YbcllN*}!4QaK4J(7D!Mfe6VdTCM>A|3sN5h_GY<k^K&=>jVjAcPx7TwB~6(+V2Ti!K}y5by~oz2#|s%zA2U<ISe|n!ASSF<QB1m&WvUz+A{8l)i`fV!XcFoqp2q}ly=|13DNQnPRdpA2e`qZWG<z5WiP@x+(8F4Az`!fRsRK6!?3ZdhD?=FU$?Zm<hOiM#KxD3J+>k*zgMmu$Kq5jH(>OZu=4uYHtV9XCEPdxq&nJPu9Nx_e_QuAm0Nw+ei}4GsdoUeWWxlLGb`mqSN=-5Z58@DAvd2Tto0kkcP=J6m>UvkH>O48UZeEjp-ic-K%4)!@ZnGf*R1|C>dA5aTwCzOamZW>+qqW?s4#GZQ=-5fhwJ7^Ew&tmTj>uZUA(-B!N{p7E7omhXvEEz&Ox4lGJaFdA@+zNa)YPV+YM8y-S4>N1_DB3}VAaOOfzPoS8Cc<)8(~bVB4@VVm6$H!hQo_Jj$;+%2NxLz8>c+eWQfL+E{qzzl_ZU~Ay=ELJ@wMr*fNGeO4c~T1*x!CB*ikuNMw`WAeA7cfKX9umFC2Qs8jHGUBf0qL;z!Df%!@5fK~<*!T^$Pq!-#Hj@HetR`S*X6@5|v^w1R`WGx!X)UxdXW{cY+f{cmBD>LBXx{Qz^Re++|2U5YLTKog5dfNiJ%__u`75w(~RmD=(mU`zMw8xcwO|Mc~0Xvv{GQN{5pht*%)wfj;j#TD)I@(<kh2Ez5l~Oai<^@DKzf8#|xJQ`GXfEMYijwOJR%ql8H72Pu&$EZ?{sl~J#JK=^Is-{JMn2zR0F?Pis+-Z|fvE1PHxOR;&ZUaRBk&|0Uo4SYOGph}r0MYKQA%G8D^N8FXMswHF@uiCGz)}pd`3AMy0fYpZ+EGxp|<IIr4lW-%B_vtNq8@+m8Rv*&@3d9AH*lc<UztD*2Xfg>^2V+K%`7EQfJ1?jk69&<q`yEF*&=mI(iu)YN191<^{qkOcd>OV!&F4MNDH>T*P=u=vE6&qzGs;H6tqs=M_0jz{d3kr*Oy9Ng#+Vyg~5p7K?Ou+z~1nR@&Sy!%@Y7>&u>@Vv!x_WF&xtx<V0(9J9hUWx9ZF5rTfg6OB0p7BzW+isEzeYF8<|HKB>TF+zS<X&?p=n*)%hRQI5onb4?VvA+8CsoQfv>9QzHQ43YedV+b%N?hKxxSfw`MnbVvesSe>)g>_?hX<zn)x@bI`CW3rkaxCb1Uct@BEu|<Vg{ZoyTT=LKs=Y5`-cypHtkm7eg%e6nl7W+D^0=`Bn#DUDkyPA_1wjnbZROjQ46W48q0omTqDQk?7_(@g3^fX(yI9a{&eKcnn43AfLKNQX<aN6wY)`<9j!VXi?z>=n1m=)0!9*UNbd%N6iHHv86U|kt-{-NT9pT@Xa~YpqRY+>7NG~WSUl@OKoVeldr`d7aqHVMNeD{VR62B=$8eo-7Os<I5U#d}ZLKXA$!4O$jM@A*uRrsaa5|L-rSiPMAjlX?Yn7IwNd1FfWA@FoY1pz#tvG>h0|Ye5We1rfHUtm|yl~$uBNfdAQDNj-6(DA}uVZQ3%%E*PiWgjpL|H_{f`LlOJfNfGNU{2=mXl>kMtc00Cx2!NalSpplJ*zo<u1`NuBKx9A0}o^rq<7`BMLC~6b6ba5I0&jgL8`;Fre#BJgHjgQN~xS18y-;FQ$IId)OYzmLP%i^VJersztV(*s5Zxz~*zPsTWbJ5BCO`?NNFQ|7OhGY8A4Gij+{{KGHlA$DJ!EcNV&U{eXujmte(T_{x#^c4bWj5zUx)FRR1DUCGUtL{1ccP_5F3l*bvocq7TRGH}0B?e4&@W<5KpTDB+gFeBV0_?&5L21Ou(xGlGFs{A)8nKQ`yCA3J(0mVxxI!~;D|J~=i`}aRS+b2(-A7kx5o~A=OfD+5)g9O;X&p&>*nOHC>nIG#CfR-Kxy_B=He*-#7$UO&xp#dIAMqObAg9-$>LUoJCDBu~L=wCU=(xs*^LAnE<H`3e|OZ7-#56N_fP+=5)0HDWVl}~LI!@17LXuh#dpP;@6r(Y-^r5@;Uk*j2l$9<`wbvfvaSJgO~Vwz+`PwFaB5XAJinyE}wiHSUMoOa9+v8}392udOyuqm&4S*o2@|3=TE;P4aSdXaG8OmA#}yL#P>&#c~jyHc;`<VBsMK+mdwW?c#kC{ma>oD$Q~edwi_<3nUfL^!3QHL>WxJ7Ps|A|_EnJ4L1u>9t68nOdK{AD&A$J3aG`hPgu@yiKuV2-ygBKXJpC>F7uxNNp=2K{*p)3+fY)6rk#cK_jFq4=cqg8bp5NEI2ReBT<ttS$?wwEM_Ylc;<SpAxaIipd3g=>yZ|=AbD6p14ucV+^|SXNzbxk^T^6une$D_Xj3JhSaKTy3K$Oa^$3bYpAuL!Ey|N@oJ2{%*A&r07M;Z0R$$iwzZZyGRVihZDpx8OAp@B(xgj&_jH#-S8ra0s3~f8IoJ6e^<d8B6naWC1bWmA43Z+l1*l=DTcKw>pYje4gN`jIj`P9p?y{tO6@M%|S3D%gseAY@P%#b2~(H!Nh))BIBf{G_zNSpGg`H=it3Z<xJ;3BSAQ*9MAX!<oqU2XI=6Ff{*)VbVM!sih2P)u9ZhGdM^gts^6sSXXHc<ilE@fqgqI{`s8bbaPzm?%XI$LEt$G<La)p=F7B*r$M|Q(G@`Ad*#FV;c;F&xwn@C7f1~KO`zMY&YEtP<qa=&bX$@B_iBaQFILhw(#U|5?Uw>!KH~r&6|wUf@Kqld=kcfXR2t)?JtBqodqVB4GnNBYDSR^nnWEkv}<$`<1I+Cs3Zc@V>CJ&COW7$6+#Eo{o@u2;zQWSk^`W8w50%KhTcmlKh#kvo(=wPq7dLo9-~v5HdsT!!c$VwjqYe|5<xDGfHVg67OkAHU9N7`sGPar?D~-$YA`E>Knj}8?2CDVc@@bg#tg_|m&rx8GvFWR-^u}>im0>2hd?uk#<FdyTJ$_F=yf&`V+BehC4Aembef7T`RLfHScHkDH7fZk#hObQ{)Z?A(}KoDScjr$6LqP3&Wu)RDWy%)A5_D3YZP)pu9&EgQ)JyU+a|hjWhGsAvt=w-US^5grJP62eR7d`v)bvTWUhbfo(HU%S+PjD&=Qn|m~+L5mKbrFTk)r8YXUoq31+~vS8;(@NbODRfO(oOv1FkP(lE_QF`M)<L(rmchKpW}Ds&=ip-*--hnk}4U8nN5d@MA~;ew{MPwG!@!j)3^B|=P&$rQX`8^_>$_12;S!d6J?Piq6wdR&vUV(n;QuQN*0o)T}3Du;ITT%}1-15MNmb~$Mo`A4Ei)mot~kn&|>dLcx~2xN8?t=NJcsKZVhC(V8kw6vuLzRd`OixL_n)DJj8Uh-{>S-t61ElO!HO~7Wh#4<<EsgPNwNM6UP&1aU=ZOkiKdr+>zwpm4ll_q2%Su|NB(@=V+-Z&|kA5dk)*10C^83-{f+XVJOwqBFPwibzW4n*To8UGZiV#Zf<LR5n1B9b5MHPEXvlFzdbIMQ1^zEX&|Tsms$9Xx1FmtKsJixQ_Yl70>PEk~cy`CS4Hi|~|aCGUjvTs9$v7FyYeQRWPb1{h9c1BDQW64j3lz>GA~Lc$$`0_lEnr2xx615Ja_-Q`+Vn)}OqpEeE#M{Psok`Fo)1DC}dR`Cf#VW=o6pQ#T~qGK_H&B>$Stjp%b={3Tx>imx_Meo3wSQ55P@6a%L0G>I4f)}IMlOvMrGUpal!%@SSE$m#UggBDb=v18>+zAs)KM~vj>=3=sDXSvJ6j&+V7>f#{d?-bhByTv1QzR%M*XkvuG%?apA_LCKf*&CsNb;f1mLb)S!*tX4ScOav%5>Cjr?+ujOeS?CYZS5PhV5SOI_rgK13hv-Hw96t^U8;aY*%(0>77~aUQcmEnkbSpRHT|{jCGoy9f?{tqEf`D;-TX(P)s4Hf(jgMm&Ga_S$f~OCVbQ^X+tdVdtPZ1FZo18tQaWu!dFtt(C8GKNaAEG%%Orq6`>}MVriNg0cKiiU|0i&m*1m@AKK0(FoVvEy_RO`K+y@~Er>>v5<R?g_Ye0tw+i<(K?maEjG!}IjMUgKtlm-u&W-BJI0C+@igAf^D3SMDOZuP=d_)kUg(WFcRtRkpP%}u0U>wS-l8Vy4aK?G&7L(4OCbiVssX?%QJP(XIDME_U7E0xhVX_F|M@fAVbYr-5OVX!fZcnByS+$jlu*{)a?cj$!UrQY|iJE}sUw6xvkpvF|#*6#Cl@F}w2_9;845`YNR7nYdkjaJ@q$fo#O(_sXGn^a9EvhC<K*tWGIO28!8%LGL=0+LI11hdbvF<Uh-CcxZTJZ~}E4kGx#whdAgW?`(u~0`t#D63mOOl7d`DZHYhq#!zpsZSin--S_yQO8-Ve=M;iDVeEievUzmsDCRlSva~$PoxB=ZEuDN17N%2?%P!n*w;ntE5rVpNe?qE~Txi!A_$CaMPy_02{{JD#E=00kBE#iXuwLI%hRW0%IcF$x(tVs6@&kbz4J}qR@8m1CXCZ=s}8tEeezpR<zAy-lkITf_dKCFjBF|B&CE|Yy?-a)!IcF93vJmJ#mFli){=^cCb<rWD*4BV}CT2)(})#YK_T3+BMJ|)>nNT`7Q#nZDfb4X+a~eK~Xc;LtnT*ZekM$J{q>V6(6pLjmEr{gcDA=mc{zzTS2QKtM55K@&qDV*y5=E8m>&s>>_Hw)yk=JN_!%EM`IthPB}|WMwY7okGY6qpb`-o%u>!zZfsJ;&(N+Yxq?(qL`-r-Au8#hD?luIppeM+De6E$JLb+}Gr<SBn)AGIoE5`Q?;LI-SI^wYr0>i|jczki@?_x03&5fZRNBi-T0UiW@C1A@c3Vu$_k-5n%o1IJILlqovmT91%Qd2>FA&O9q!tb-1cO!(%(@heT23RKu(m3x!_geGq@ZUYhT>PxN%>!m402b0C{KJ>=-%XmQayu&%=g>jDzUr@uNGSs+)=Cpm#fa<<<MKql~fLm24|=7HmL9?yM$~zT&<^^HOmoS(h#9EayB4HEk4x*Q`A&athGRcCZqVPTzwNUpQXEBia~!mP<-Zt>djLe`(~HPrEU`AQ_D<Nniw(65~Oq*O|5cT`3|6bOSY`*>=H#<Q4BRF8kNHf&@1!`tjNGlH7#a-#M>ag4vIh|%MocU0Gb>*CcGA>pT<Z_3Uz_YK0@`Pk)yw%KTa(;wBDHlKl_#rq5z11nhcamYy)qZNQz~dij7k>Z9_C_=49seZE1r+oR&z?fp5=$$FEHz1hZ7emo(()!<&BsESow1n8whSLh<YU%cyThLXAYi{v_TMI(Ms#cUP#!NNQ_VM31gB@_4)d?*0c(Djk>')).decode("utf-8"))
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


def _front_run(action, obs, state, step):
    if not _FR_ITEMS:
        return action
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    moved = {}
    action = _copy_action(action)
    for item in _FR_ITEMS:
        target = _future_quantity(step, item)
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


_R5_EXTRA_COW = False
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

    if 160 <= step <= 210 or (_R5_EXTRA_COW and 500 <= step <= 525):
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


def _guarded_demand_cow9(obs, action, step):
    if not _R5_EXTRA_COW or step != 289 or _owned_cows(obs) != 8:
        return action
    shops = list(
        _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    )
    milk_demand = sum(
        shop in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
        for shop in shops
    )
    farm = _farm(obs, _seat(obs))
    if milk_demand < 2 or float(_get(farm, "money", 0) or 0) < 800:
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



# V3B adds a second-order market counter derived from the public
# "Kaggriculture Breaking the Tie" policy.  Only its premium-sale schedule is
# retained here; field actions and terminal policy come from the 8C/4S route.
_META_SALES = {160: {'WOOL': 9}, 168: {'WOOL': 17}, 233: {'MILK': 3}, 240: {'WOOL': 18}, 252: {'MELON': 10}, 255: {'MELON': 6}, 257: {'MELON': 11}, 260: {'MELON': 6}, 262: {'MELON': 6}, 302: {'MILK': 6}, 330: {'MILK': 3}, 335: {'MILK': 4}, 358: {'MILK': 13}, 361: {'WOOL': 8, 'MILK': 3}, 362: {'MILK': 6}, 377: {'MILK': 12}, 380: {'WOOL': 8}, 386: {'STRAWBERRY': 2}, 389: {'MILK': 3}, 400: {'STRAWBERRY': 8}, 405: {'STRAWBERRY': 14}, 406: {'MILK': 24}, 419: {'WOOL': 12}, 423: {'STRAWBERRY': 2}, 427: {'WOOL': 13}, 430: {'MILK': 3}, 431: {'MILK': 7}, 432: {'STRAWBERRY': 28}, 451: {'MILK': 8}, 453: {'WOOL': 12}, 455: {'MILK': 9}, 470: {'MILK': 3}, 472: {'STRAWBERRY': 12}, 479: {'STRAWBERRY': 16}, 480: {'STRAWBERRY': 20, 'MILK': 6}, 484: {'MILK': 7}, 486: {'MELON': 6}, 488: {'MELON': 6}, 490: {'MELON': 12}, 492: {'MELON': 6}, 493: {'MELON': 10}, 495: {'MELON': 6}, 496: {'MELON': 6}, 502: {'MELON': 15, 'MILK': 9}, 503: {'MELON': 6}, 504: {'STRAWBERRY': 18, 'MELON': 14}, 513: {'MILK': 3}, 519: {'MILK': 3}, 522: {'STRAWBERRY': 10}, 523: {'MILK': 14}, 527: {'STRAWBERRY': 4}, 528: {'STRAWBERRY': 30}, 551: {'MILK': 13}, 552: {'STRAWBERRY': 24}, 553: {'MILK': 8}, 555: {'MILK': 9}, 559: {'MILK': 3}, 568: {'WOOL': 8}, 575: {'STRAWBERRY': 13}, 583: {'WOOL': 8}, 587: {'MILK': 10}, 593: {'MILK': 4}, 594: {'STRAWBERRY': 20}, 599: {'MILK': 12}, 609: {'STRAWBERRY': 17}, 615: {'STRAWBERRY': 13}, 618: {'MILK': 8}, 621: {'MILK': 4}, 634: {'WOOL': 6}, 638: {'MILK': 10}, 645: {'STRAWBERRY': 16}, 648: {'MILK': 7}, 651: {'STRAWBERRY': 11}, 661: {'WOOL': 10}, 665: {'MILK': 12}, 666: {'MILK': 9}, 669: {'WOOL': 17}, 682: {'WOOL': 8}, 690: {'MILK': 8}, 701: {'STRAWBERRY': 22}, 702: {'MILK': 18}, 703: {'MILK': 18}, 715: {'MILK': 18}}
_META_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_META_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_META_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_META_HORIZON = 4


def _new_meta_state():
    return {
        "last_step": -1,
        "clone_confidence": 0,
        "h4_active": False,
        "h4_evidence": 0,
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
    target = step + 5
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
    return True


def _meta_front_run(action, obs, step, state):
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


def agent(obs, config=None):
    """Return the V3B action for one Kaggriculture observation."""
    try:
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

        action = _weed_repair_action(
            obs,
            _copy_action(_ACTIONS[step]),
            step,
        )
        action = _cow_place_alignment(obs, action, step)
        action = _guarded_demand_cow9(obs, action, step)
        state = _fr_state(obs, step)
        action = _repay(action, state, step)
        action = _front_run(action, obs, state, step)
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
