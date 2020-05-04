import random

def random_int(num1=0, num2=100):
    return(f'Randoming from {str(num1)} to {str(num2)} : {random.randint(num1,num2)}')

def random_ask(question):
    responses = ["O itu pasti.",
                "Kelihatannya begitu",
                "Bukan maen.",
                "Jelas jelas iya.",
                "Coba Anda pikirkan sendiri.",
                "Kelihatannya iya.",
                "Most likely.",
                "Pandangan baik.",
                "Ya.",
                "Tanda mengarah ke iya.",
                "Ga yakin, Coba lagi.",
                "Coba lagi nanti.",
                "Lebih baik tidak memberitahumu.",
                "Tidak bisa prediksi sekarang.",
                "Fokus dan tanyakan lagi.",
                "Jangan percaya.",
                "Jawabanku tidak.",
                "Sumberku mengatakan tidak.",
                "Pandangan tidak baik.",
                "Sangat ragu."]
    return(f'Question: {question}\nAnswer: {random.choice(responses)}')