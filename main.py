from pygame.locals import *
import pygame
from random import randint



def reset_food():
	# Reseta a posição da comida
	return (randint(0, (SCREEN_WIDTH-10)//10)*10, randint(0, (SCREEN_HEIGHT-10)//10)*10)


def snake_is_die(snk):
	# Verifica se a cobrinha morreu
	snake_head = snake[0]
	result = False
	if 0 < snake_head[0] < SCREEN_WIDTH and 0 < snake_head[1] < SCREEN_HEIGHT:
		pass
	else:
		result = True # Morreu ao sair da tela
	for snake_bd in snake[1:]:
		if snake_head[0] == snake_bd[0] and snake_head[1] == snake_bd[1]:
			result = True # Morreu ao comer o próprio rabo
	return result

def import_record():
	# Importando o record, salvo externamente
	arq = open("score.txt")
	record_save = arq.read()
	arq.close()
	try:
		record_save = int(record_save)
	except:
		record_save = 0
	else:
		pass
	finally:
		return record_save

def export_record(num):
	# Exportando o record atual
	arq = open("score.txt", "w")
	arq.write(str(num))
	arq.close()

# Iniciando pygame
pygame.init()

# Criando a janela do programa
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instanciando o metodo limitador de FPS
clock = pygame.time.Clock()
fps = 30

# Cores a serem usadas
snake_color_1 = (255, 255, 255)
snake_color_2 = (255, 0, 0)
screen_bg = (255, 255, 255)
screen_bg = (0, 0, 0)
food_color = (0, 255, 0)
score_color = (255, 255, 255)

# Variaveis da cobrinha

snake = [[x, 300] for x in range(300, 100, -10)]
snake_body = 3
snake_size = 10
snake_speed = 10

# Movimendos da cobrinha
# {tecla_movimendo: (fator_movimento, eixo_movimento, tecla_contraria)}
move_set = {K_a: (-1, 0, K_d), 
			K_d: (1, 0, K_a),
			K_w: (-1, 1, K_s),
			K_s: (1, 1, K_w)}
move = K_d

# Variáveis e funções da comida
food_size = 10
food_pos = reset_food()

# Pontuação
score = 0
record = import_record()
# Fonte para exibir a pontuação
font = pygame.font.Font(None, 30)

# Laço onde o game ocorre
run = True
while run:
	# Laço de eventos
	for event in pygame.event.get():
		if event.type == QUIT:
			run = False
		if event.type == KEYDOWN: # Verifica se alguma tecla foi pressionada
			if event.key in move_set: # Verifica se a pressionada é um movimento válido
				# Define a direção da cobrinha, desde que a nova direção não seja para tras
				move = event.key if event.key != move_set[move][2] else move
	# Limpa a tela
	screen.fill(screen_bg)

	# Salva a posição antiga da cabeça da cobrinha para uso futuro
	snake_old_head = snake[0][:]

	# Movimenta a cabeça da cobra
	snake[0][move_set[move][1]] += snake_speed * move_set[move][0]

	# Mostra pontuação na tela
	score_text = font.render(f"Score   {score:0>3}", True, score_color)
	screen.blit(score_text, (10, 10))
	record_text = font.render(f"Record {record:0>3}", True, score_color)
	screen.blit(record_text, (10, 40))

	# Desenha a cabeça da cobra
	snake_head_rect = pygame.draw.rect(screen, snake_color_2, (snake[0][0], snake[0][1], snake_size, snake_size))

	# Desenha a comida na tela
	food_rect = pygame.draw.rect(screen, food_color, (food_pos[0], food_pos[1], food_size, food_size))

	# Testa se a cobrinha chegou até a comidinha
	if snake_head_rect.colliderect(food_rect):
		score += 1
		food_pos = reset_food()
		snake.append([0, 0])
		if score > record:
			record = score

	# Cria o restante do corpo da cobrinha com base na posição antiga da cabeça da cobrinha
	for snake_bd in snake[1:]:
		snake_old_bd = snake_bd[:]
		snake_bd[0], snake_bd[1] = snake_old_head[0], snake_old_head[1] 
		pygame.draw.rect(screen, snake_color_1, (snake_bd[0], snake_bd[1], snake_size, snake_size))
		snake_old_head = snake_old_bd

	# Testa se a cobrinha morreu
	if snake_is_die(snake):
		run =  False
	
	clock.tick(fps)
	pygame.display.update()


# Exportando a pontuação
export_record(record)

# Finalizando o pygame
pygame.quit()