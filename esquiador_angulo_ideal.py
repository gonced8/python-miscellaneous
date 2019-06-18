from math import cos, sin, tan, degrees, radians, pi, log10

x=' '

while x==' ':
    
    precisao = 1    # INVERSO - Precisão do resultado do ângulo em graus
    da = radians(precisao/1)
    dt = precisao/(10**3)  #Precisão da simulação

    alfa = 0    # Ângulo da rampa
    ALFA = 0    # Melhor ângulo

    beta=pi/2
    while(beta>=pi/2):
        beta = radians(float(input('Ângulo da montanha: ')))   # Ângulo da encosta

    dist = -1    # Distância percorrida na horizontal

    t = 0
    velocidade = 10     # Velocidade inicial do esquiador

    corpo = {'aceleracao_x': 0, 'aceleracao_y': -9.81,
             'velocidade_x': 0, 'velocidade_y': 0,
             'posicao_x': 0, 'posicao_y': 0}

    plano = {'posicao_y': 0,
             'declive': -tan(beta)}
        
    alfa = alfa-da

    while (alfa <= pi/2):

        alfa = alfa + da
        #print('\n', degrees(alfa))
        t=0
        corpo['posicao_x'] = 0
        corpo['posicao_y'] = 0
        corpo['velocidade_x'] = velocidade*cos(alfa)
        corpo['velocidade_y'] = velocidade*sin(alfa)

        while True:
            
            t = t + dt
            
            if(corpo['velocidade_x']!=0 or corpo['aceleracao_x']!=0):
                corpo['posicao_x'] = corpo['velocidade_x']*t + corpo['aceleracao_x']*t*t/2

            if(corpo['velocidade_y']!=0 or corpo['aceleracao_y']!=0):
                corpo['posicao_y'] = corpo['velocidade_y']*t + corpo['aceleracao_y']*t*t/2


            plano['posicao_y'] = corpo['posicao_x']*plano['declive']

            #print(corpo['posicao_x'], corpo['posicao_y'],  plano['posicao_y'])

            if(corpo['posicao_y']<plano['posicao_y']):
                break

        t = t - dt
        corpo['posicao_x'] = corpo['velocidade_x']*t + corpo['aceleracao_x']*t*t/2
        
        if(corpo['posicao_x']>=dist):
            dist=corpo['posicao_x']
            ALFA = alfa
            
        '''else:
            if(t>dt):
                break'''


    if (ALFA <= pi/2):
        print("Ângulo ideal:", round(degrees(ALFA), int(-log10(precisao))))
        print("Teórico:", degrees(pi/4 - beta/2))

    else:
        print("Não foi possível determinar o melhor ângulo...")

    x=input("Prima <ESPAÇO><ENTER> para repetir ou <ENTER> para fechar")
    print('\n')
