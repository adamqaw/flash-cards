from tkinter import *
import pandas as pd
import random

# ---------------------------------- COMMANDS --------------------------------------- #
to_learn = {}
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")

    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
card = {}


def next_card():
    global card, flip_timer
    window.after_cancel(flip_timer)
    card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=card["French"])
    canvas.itemconfig(canvas_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=card["English"])
    canvas.itemconfig(canvas_image, image=card_back_image)


# -------------------------------- SAVE PROGRESS ------------------------------------#
def correct_card():
    to_learn.remove(card)
    correct_data = pd.DataFrame(to_learn)
    correct_data.to_csv("data/learned_words.csv", index=False)
    next_card()


# ---------------------------------- UI SETUP ---------------------------------------#
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash Card App")

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas()
canvas.config(height=530, width=850)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(425, 265, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = canvas.create_text(420, 80, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text((420, 250), text="word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

correct_button_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_button_image, highlightthickness=0, command=correct_card)
correct_button.config(width=75, height=75)
correct_button.grid(row=1, column=0)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=next_card)
wrong_button.config(width=75, height=75)
wrong_button.grid(row=1, column=1)

next_card()

window.mainloop()
