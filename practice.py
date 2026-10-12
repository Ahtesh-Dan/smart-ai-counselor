print("Aks University scholarship checker me aap ka swagat hai!")

# input() ko int() mein wrap kiya taaki text number ban jaye
student_percentage = int(input("Please write your percentage: "))

# Sahi variable name aur comparison
if student_percentage >= 85:
    print("Congratulations! Aapko 20% Scholarship milti hai.")
else:
    print("Aapko normal fees pay karni hogi.")
