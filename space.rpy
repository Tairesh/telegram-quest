label start
	Привет!
	Нужно что-то выбрать
	menu
		Хороший выбор
			jump good_ending
		Плохой выбор
			jump bad_ending

label good_ending
	Хорошая концовка
	Прям ваще
	return

label bad_ending
	Плохая концовка
	return