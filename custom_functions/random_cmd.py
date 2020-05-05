import random

def random_int(num1=0, num2=100):
    return(f'Mengacak angka {str(num1)} sampai {str(num2)} : {random.randint(num1,num2)}')

def random_ask(question):
    responses = ["O itu pasti.",
                "Kelihatannya begitu",
                "Bukan maen.",
                "Jelas jelas iya.",
                "Coba Anda pikirkan sendiri.",
                "Kelihatannya iya.",
                "Mendekati.",
                "Hasilnya baik.",
                "Ya.",
                "Tanda mengarah ke iya.",
                "Ga yakin, Coba lagi.",
                "Coba lagi nanti.",
                "O tidak bisa.",
                "Lebih baik tidak memberitahumu.",
                "Tidak bisa prediksi sekarang.",
                "Fokus dan tanyakan lagi.",
                "Jangan percaya.",
                "Jawabanku tidak.",
                "Sumberku mengatakan tidak.",
                "Hasilnya tidak baik.",
                "Penuh keraguan."]
    return(f'Nanya: {question}\nJawab: {random.choice(responses)}')