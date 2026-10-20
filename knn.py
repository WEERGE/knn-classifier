import json
import math


def read_point(prompt):
    while True:
        try:
            x = float(input(f'Введите координату {prompt} по оси x: '))
            y = float(input(f'Введите координату {prompt} по оси y: '))
            return (x, y)
        except ValueError:
            print("Ошибка: введите число.")


def collect_points():
    data = {}

    while True:
        point = read_point("точки")
        label = input("Введите метку класса объекта: ").strip()

        if label not in data:
            data[label] = []

        if point in data[label]:
            print(f"Ошибка: точка {point} уже есть в классе '{label}'. Введите другую точку.")
            continue

        data[label].append(point)

        if len(data) >= 2:
            ok = True
            for lbl in data:
                if len(data[lbl]) < 3:
                    ok = False
                    break

            if ok:
                cont = input("Добавить ещё одну точку? (y — да, любой другой символ — нет): ")
                if cont.lower() != 'y':
                    break
            else:
                print("Для каждой метки требуется минимум 3 точки.")
        else:
            print("Требуется минимум 2 различных метки классов.")

    return data


def read_k(total):
    while True:
        try:
            k = int(input(f"Введите количество ближайших соседей k (1..{total}): "))
            if 1 <= k <= total:
                return k
            print(f"Ошибка: k должно быть от 1 до {total}.")
        except ValueError:
            print("Ошибка: введите целое число.")


def distance(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def neighbours(data, point, k):
    all_points = []
    for label, points in data.items():
        for p in points:
            all_points.append((distance(point, p), label, p))

    all_points.sort(key=lambda x: x[0])
    return all_points[:k]


def predict(data, point, k):
    nearest = neighbours(data, point, k)

    votes = {}
    for _, label, _ in nearest:
        votes[label] = votes.get(label, 0) + 1

    max_votes = max(votes.values())
    candidates = [label for label, count in votes.items() if count == max_votes]

    if len(candidates) > 1:
        for _, label, _ in nearest:
            if label in candidates:
                return label

    return candidates[0]


def save_data(data, path):
    plain = {label: [list(p) for p in points] for label, points in data.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plain, f, ensure_ascii=False)


def load_data(path):
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return {label: [tuple(p) for p in points] for label, points in raw.items()}


DATA_FILE = "data.json"


def main():
    data = load_data(DATA_FILE)

    if data is not None:
        total = sum(len(p) for p in data.values())
        answer = input(f"Найдена сохранённая выборка ({total} точек). "
                       f"Использовать? (y/n): ")
        if answer.strip().lower() != "y":
            data = None

    if data is None:
        data = collect_points()
        save_data(data, DATA_FILE)

    total = sum(len(p) for p in data.values())
    print(f"Введено {total} точек, метки классов: "
          f"{', '.join(sorted(set(data)))}")

    unknown = read_point("Введите координаты точки неизвестного класса.")
    k = read_k(total)

    print(f"Ближайшие соседи точки {unknown}:")
    for dist_sq, label, p in neighbours(data, unknown, k):
        print(f"({p[0]:.1f}, {p[1]:.1f})  расстояние {math.sqrt(dist_sq):.2f}  метка {label}")

    print("Предсказанная метка класса:", predict(data, unknown, k))


if __name__ == '__main__':
    main()