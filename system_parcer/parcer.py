import subprocess
import datetime


# Функция для запуска команды ps aux и получения вывода
def get_process_data():
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode().split('\n')


# Функция для парсинга данных о процессах
def parse_process_data(process_data):
    user_processes = {}
    total_processes = 0
    total_memory = 0
    total_cpu = 0
    max_memory_process = ('', 0)
    max_cpu_process = ('', 0)

    for line in process_data:
        parts = line.split()
        if len(parts) >= 11:
            user = parts[0]
            user_processes[user] = user_processes.get(user, 0) + 1
            total_processes += 1
            try:
                memory = float(parts[5])
                cpu = float(parts[2])
            except ValueError:
                continue

            total_memory += memory
            total_cpu += cpu

            if memory > max_memory_process[1]:
                max_memory_process = (parts[10][:20], memory)
            if cpu > max_cpu_process[1]:
                max_cpu_process = (parts[10][:20], cpu)

    return user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process


# Функция для форматированного вывода данных
def print_report(user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process):
    print("Отчёт о состоянии системы:")
    print("Пользователи системы:", list(user_processes.keys()))
    print("Процессов запущено:", total_processes)
    print("\nПользовательских процессов:")
    for user, processes in user_processes.items():
        print(f"{user}: {processes}")
    print("\nВсего памяти используется: {:.1f}%".format(total_memory))
    print("Всего CPU используется: {:.1f}%".format(total_cpu))
    print("Больше всего памяти использует:", max_memory_process[0], "({:.1f}%)".format(max_memory_process[1]))
    print("Больше всего CPU использует:", max_cpu_process[0], "({:.1f}%)".format(max_cpu_process[1]))


# Функция для сохранения отчета в файл
def save_report_to_file(user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process):
    current_datetime = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f"{current_datetime}-scan.txt"
    with open(filename, 'w') as f:
        f.write("Отчёт о состоянии системы:\n")
        f.write("Пользователи системы: {}\n".format(list(user_processes.keys())))
        f.write("Процессов запущено: {}\n\n".format(total_processes))
        f.write("Пользовательских процессов:\n")
        for user, processes in user_processes.items():
            f.write("{}: {}\n".format(user, processes))
        f.write("\nВсего памяти используется: {:.1f}%\n".format(total_memory))
        f.write("Всего CPU используется: {:.1f}%\n".format(total_cpu))
        f.write("Больше всего памяти использует: {} ({:.1f}%)\n".format(max_memory_process[0], max_memory_process[1]))
        f.write("Больше всего CPU использует: {} ({:.1f}%)\n".format(max_cpu_process[0], max_cpu_process[1]))
    print("Отчёт сохранен в файл:", filename)


process_data = get_process_data()
user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process = parse_process_data(
    process_data)
print_report(user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process)
save_report_to_file(user_processes, total_processes, total_memory, total_cpu, max_memory_process, max_cpu_process)
