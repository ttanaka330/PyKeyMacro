import tkinter as tk
import threading
from input_code import Input
from key_input import KeyInput
from key_output import KeyOutput

MODE_DEFAULT = 0
MODE_INPUT = 1
MODE_OUTPUT = 2

DEFAULT_INTERVAL = 100


class AppFrame(tk.Frame):
    def __init__(self, master: tk.Misc = None) -> None:
        super().__init__(master)
        self.master.title("PyKeyMacro")
        self.master.geometry("400x300")
        self.master.minsize(width=400, height=300)
        self.__create_status_bar()
        self.__create_side_menu()
        self.__create_content()
        self.__create_listener()
        self.__update_state_default()

    def __create_status_bar(self):
        status_bar = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        value_message = tk.StringVar()
        messagebox = tk.Label(status_bar, textvariable=value_message)

        messagebox.pack(side=tk.LEFT)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.frame_status_bar = status_bar
        self.value_message = value_message

    def __create_side_menu(self):
        side_menu = tk.Frame(self.master, width=120, pady=5, padx=5)
        button_input = tk.Button(side_menu, command=self.__on_input)
        button_output = tk.Button(side_menu, command=self.__on_output)
        button_clear = tk.Button(side_menu, command=self.__on_clear)

        check_value = tk.BooleanVar(value=True)
        check_loop = tk.Checkbutton(side_menu,
                                    text="繰り返し再生",
                                    variable=check_value)

        frame_interval = tk.Frame(side_menu)
        label_interval = tk.Label(frame_interval, text="キー間隔")
        value_interval = tk.IntVar(value=DEFAULT_INTERVAL)
        entry_interval = tk.Entry(frame_interval,
                                  width=5,
                                  textvariable=value_interval)
        label_interval_unit = tk.Label(frame_interval, text="ms")
        label_interval.pack(side=tk.LEFT)
        entry_interval.pack(side=tk.LEFT)
        label_interval_unit.pack(side=tk.LEFT)

        button_input.pack(side=tk.TOP, fill=tk.X)
        check_loop.pack(side=tk.TOP, anchor=tk.W, pady=(20, 0))
        frame_interval.pack(side=tk.TOP)
        button_output.pack(side=tk.TOP, fill=tk.X)
        button_clear.pack(side=tk.TOP, pady=(20, 0), fill=tk.X)
        side_menu.pack(side=tk.LEFT, fill=tk.Y)
        side_menu.propagate(0)

        self.frame_side_menu = side_menu
        self.button_input = button_input
        self.button_output = button_output
        self.button_clear = button_clear
        self.check_value = check_value
        self.value_interval = value_interval

    def __create_content(self):
        content = tk.Frame(self.master, borderwidth=2, relief=tk.SUNKEN)
        value_input = tk.StringVar()
        inputbox = tk.Listbox(content,
                              font=("Courier", 10),  # 等幅フォント
                              listvariable=value_input,
                              selectmode=tk.EXTENDED)
        scrollbar = tk.Scrollbar(content,
                                 orient=tk.VERTICAL,
                                 command=inputbox.yview)
        inputbox["yscrollcommand"] = scrollbar.set

        inputbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, after=inputbox, fill=tk.Y)
        content.pack(after=self.frame_side_menu, fill=tk.BOTH, expand=True)

        self.frame_content = content
        self.inputbox = inputbox
        self.value_input = value_input
        self.recorded: list[Input] = []

    def __create_listener(self):
        self.key_input = KeyInput(self.__callback_input)
        self.key_output = KeyOutput(self.__callback_output_completed)

    def __callback_input(self, result: Input):
        self.recorded.append(result)
        self.value_input.set(self.recorded)
        self.inputbox.yview_moveto(1)

    def __callback_output_completed(self):
        self.__update_state_default()

    def __is_mode_input(self) -> bool:
        return self.type == MODE_INPUT

    def __is_mode_output(self) -> bool:
        return self.type == MODE_OUTPUT

    def __update_state_default(self):
        self.type = MODE_DEFAULT
        self.__set_button_start(self.button_input, "入力")
        if len(self.recorded) == 0:
            self.__set_button_disable(self.button_output, "再生")
        else:
            self.__set_button_start(self.button_output, "再生")
        self.__set_button_start(self.button_clear, "クリア")
        self.inputbox["state"] = tk.NORMAL
        self.value_message.set("")

    def __update_state_input(self):
        self.type = MODE_INPUT
        self.__set_button_stop(self.button_input, "停止")
        self.__set_button_disable(self.button_output, "再生")
        self.__set_button_disable(self.button_clear, "クリア")
        self.inputbox["state"] = tk.DISABLED
        self.value_message.set("キー登録中。")

    def __update_state_output(self):
        self.type = MODE_OUTPUT
        self.__set_button_disable(self.button_input, "入力")
        self.__set_button_stop(self.button_output, "停止")
        self.__set_button_disable(self.button_clear, "クリア")
        self.inputbox["state"] = tk.DISABLED
        self.value_message.set("キー再生中。Escで再生を中止します。")

    def __set_button_start(self, button: tk.Button, text: str):
        button["text"] = text
        button["fg"] = "#000000"
        button["state"] = tk.NORMAL

    def __set_button_stop(self, button: tk.Button, text: str):
        button["text"] = text
        button["fg"] = "#FF8080"
        button["state"] = tk.NORMAL

    def __set_button_disable(self, button: tk.Button, text: str):
        button["text"] = text
        button["state"] = tk.DISABLED

    def __on_input(self):
        if self.__is_mode_input():
            self.key_input.stop_input()
            self.__update_state_default()
            self.__remove_last_input()
        else:
            self.key_input.start_input()
            self.__update_state_input()

    def __on_output(self):
        if self.__is_mode_output():
            self.key_output.stop_output()
            self.__update_state_default()
        else:
            self.__update_state_output()
            thread = threading.Thread(target=self.__start_output)
            thread.start()

    def __start_output(self):
        try:
            interval = self.value_interval.get()
        except tk.TclError:
            interval = 0
        self.key_output.start_output(
            self.recorded, interval, self.check_value.get())

    def __on_clear(self):
        self.recorded.clear()
        self.value_input.set(self.recorded)

    def __remove_last_input(self):
        del self.recorded[-1]
        self.value_input.set(self.recorded)
