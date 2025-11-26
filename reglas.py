# reglas.py
from experta import *
from hechos import *

class SistemaEducativo(KnowledgeEngine):

    # 1
    @Rule(Perfil(AB=True), Perfil(AG=True))
    def r1(self):
        self.declare(A())
    
    # 2
    @Rule(Perfil(AB=True))
    def r2(self):
        self.declare(FF())

    # 3
    @Rule(FF())
    def r3(self):
        self.declare(E(), V())

    # 4
    @Rule(Perfil(AG=True))
    def r4(self):
        self.declare(B(), C(), D(), AA())


    # 5
    @Rule(Perfil(AH=True))
    def r5(self):
        self.declare(I(), K())

    # 6
    @Rule(K())
    def r6(self):
        self.declare(X())

    # 7
    @Rule(Perfil(AF=True))
    def r7(self):
        self.declare(F(), T(), U(), LL())

    # 8
    @Rule(Perfil(AD=True))
    def r8(self):
        self.declare(L(), M())

    # 9
    @Rule(Perfil(AC=True))
    def r9(self):
        self.declare(M(), N())


    # 10
    @Rule(O())
    def r10(self):
        self.declare(S(), R())


    # 11
    @Rule(Perfil(AI=True))
    def r11(self):
        self.declare(AA(), DD())

    # 12
    @Rule(Perfil(AI=True), Perfil(AG=True))
    def r12(self):
        self.declare(GG())

    # 13
    @Rule(DD())
    def r13(self):
        self.declare(EE())


    # 14
    @Rule(Perfil(AB=True), Perfil(AF=True), Perfil(AI=True))
    def r14(self):
        self.declare(BB())

    # 15
    @Rule(BB())
    def r15(self):
        self.declare(CC())


    # 16
    @Rule(Perfil(AE=True), Perfil(AG=True))
    def r16(self):
        self.declare(KK(), GG())

    # 17
    @Rule(GG())
    def r17(self):
        self.declare(HH(), K(), II())

    # 18
    @Rule(HH())
    def r18(self):
        self.declare(JJ(), M(), N())


    # 19
    @Rule(Perfil(AI=True), Perfil(AH=True))
    def r19(self):
        self.declare(LL(), MM())

    # 20
    @Rule(Perfil(AI=True), GG())
    def r20(self):
        self.declare(NN())

    # 21
    @Rule(LL())
    def r21(self):
        self.declare(OO())

    # 22
    @Rule(MM())
    def r22(self):
        self.declare(A())


    # 23
    @Rule(Perfil(AE=True), Perfil(AF=True))
    def r23(self):
        self.declare(BB())

    # 24
    @Rule(BB())
    def r24(self):
        self.declare(HH(), RR())

    # 25
    @Rule(HH())
    def r25(self):
        self.declare(N(), M())


    # 26
    @Rule(Perfil(AF=True), Perfil(AC=True), Perfil(AD=True))
    def r26(self):
        self.declare(QQ())

    # 27
    @Rule(QQ())
    def r27(self):
        self.declare(G())

    # 28
    @Rule(Perfil(AC=True), Perfil(AE=True))
    def r28(self):
        self.declare(QQ())

    