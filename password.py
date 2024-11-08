import random
import string
import customtkinter
from CTkMessagebox import CTkMessagebox


class PasswordGeneratorApp:
    def __init__(self):

        # Crear ventana principal
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.root = customtkinter.CTk()
        self.root.geometry("500x450")
        self.root.title("Password Generator App")

        # Crear el marco principal
        # no usamos .self ya que NO vamos a necesitar modificar esta variable desde otro metodo
        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Crear y configurar los widgets
        label = customtkinter.CTkLabel(
            master=frame, text="Password Generator", font=("Arial", 20))
        label.pack(pady=12, padx=10)

        label2 = customtkinter.CTkLabel(
            master=frame, text="Length of your password:", font=("Arial", 16))
        label2.pack(pady=1, padx=10)

        self.slider = customtkinter.CTkSlider(
            master=frame, from_=0, to=50, number_of_steps=50, command=self.slider_event)
        self.slider.pack(pady=12, padx=10)

        self.entry = customtkinter.CTkEntry(master=frame, width=50)
        self.entry.pack(pady=10, padx=10)
        self.entry.bind("<KeyRelease>", self.on_entry_change)

        # Crear un marco para los checkboxes y agregarlo al contenedor principal
        checkbox_frame = customtkinter.CTkFrame(master=frame)
        checkbox_frame.pack(pady=6, padx=5, fill="x")

        self.checkbox_numbers = customtkinter.CTkCheckBox(
            master=checkbox_frame, text="Numbers")
        self.checkbox_numbers .pack(side="left", padx=5, pady=10)

        self.checkbox_upper = customtkinter.CTkCheckBox(
            master=checkbox_frame, text="Uppercase")
        self.checkbox_upper .pack(side="left", padx=5, pady=10)

        self.checkbox_lower = customtkinter.CTkCheckBox(
            master=checkbox_frame, text="Lowercase")
        self.checkbox_lower .pack(side="left", padx=5, pady=10)

        self.checkbox_symbols = customtkinter.CTkCheckBox(
            master=checkbox_frame, text="Symbols")
        self.checkbox_symbols .pack(side="left", padx=5, pady=10)

        button = customtkinter.CTkButton(
            master=frame, text="Generate Password", command=self.get_user_input)
        button.pack(pady=10, padx=10)

        self.entry2 = customtkinter.CTkEntry(
            master=frame, width=250, state="disabled")
        self.entry2.pack(pady=10, padx=10)

        # Añade un botón para copiar la contraseña
        self.copy_button = customtkinter.CTkButton(
            master=frame, text="Copy Password", command=self.copy_password)
        self.copy_button.pack(pady=5, padx=10)

    # _ es un parámetro que se utiliza para capturar el evento que se dispara cuando el
    # contenido del campo de texto (Entry) cambia
    # No se usa dentro de la función, pero es necesario incluirlo para que la
    # vinculación del evento funcione correctamente.
    # es una convención común en Python cuando se quiere indicar que un argumento
    # no se va a usar dentro de la función. Es decir, el guion bajo le dice a
    # otros programadores (o incluso a ti mismo en el futuro) que el valor
    # del parámetro no es importante para el funcionamiento de la función.
    # En tu caso, el evento que se dispara al cambiar el contenido del Entry
    # pasa automáticamente un objeto de evento al método on_entry_change.
    # Aunque no lo uses dentro de la función, debes incluirlo para que la función
    # esté correctamente definida y pueda ser vinculada al evento del widget.
    # Así que _ actúa simplemente como un marcador de posición.
    # Si en algún momento necesitas usar el objeto de evento para obtener
    # más información (como la tecla que se presionó), podrías darle
    # un nombre más significativo y utilizarlo en el código
    def on_entry_change(self, _):
        """ Actualizar el valor del Entry manualmente por teclado """
        try:
            value_str = self.entry.get()
            # Si value_str no está vacío (if value_str), se convierte a un número
            # entero usando int(value_str) y se asigna a la variable value
            # Si value_str está vacío (por ejemplo, si el usuario ha borrado todo
            # el contenido del Entry), se asigna 0 a value
            value = int(value_str) if value_str else 0
            if value <= 0:
                value = 0
            elif value >= 50:
                value = 50
            self.slider.set(value)
        except ValueError:
            CTkMessagebox(title="Error", message="No has introducido un valor numerico",
                                icon="cancel")

    def slider_event(self, value):
        """ Actualizar el valor del Entry con el valor del slider """
        # primer parametro es el indice de inicio desde el que se borrará,
        # el segundo indica hasta donde se borrará
        self.entry.delete(0, customtkinter.END)
        # primer parametro indica desde qué indice se quiere añadir este nuevo valor,
        # el segundo es el valor a añadir
        # se convierte primero a int porque NO queremos flotantes
        self.entry.insert(0, str(int(value)))

    def get_user_input(self):
        """Obtener y validar la longitud de la contraseña.
        Preguntar si se deben incluir números y caracteres especiales"""
        password_length = int(self.slider.get())
        numbers = self.checkbox_numbers.get()
        upper = self.checkbox_upper.get()
        lower = self.checkbox_lower.get()
        symbols = self.checkbox_symbols.get()
        self.generate_password(password_length,
                               numbers, upper, lower, symbols)

    def generate_password(self, password_length, numbers, upper, lower, symbols):
        """Crear y retornar la lista de caracteres permitidos"""
        chars = ""
        if numbers:
            chars += string.digits
        if upper:
            chars += string.ascii_uppercase
        if lower:
            chars += string.ascii_lowercase
        if symbols:
            chars += string.punctuation

        try:
            selection = random.choices(chars, k=password_length)
            if selection:
                password = "".join(selection)

                print(password)
                # Actualizar entry2 con el valor de la contraseña generada
                # Habilitar el Entry para modificarlo
                self.entry2.configure(state="normal")
                self.entry2.delete(0, customtkinter.END)
                self.entry2.insert(0, str(password))
                # Volver a deshabilitar el Entry
                self.entry2.configure(state="disabled")

        except IndexError:
            CTkMessagebox(title="Error", message="No has seleccionado ninguna opcion",
                                icon="cancel")

    def copy_password(self):
        """Habilitar la función de copiar la contraseña"""
        self.entry2.configure(
            state="normal")  # Habilitar temporalmente el Entry
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry2.get())
        # Volver a deshabilitar el Entry
        self.entry2.configure(state="disabled")
        CTkMessagebox(title="Copied", message="Password copied to clipboard!")

    def run(self):
        """run the app"""
        self.root.mainloop()


def main():
    """main function"""
    app = PasswordGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
