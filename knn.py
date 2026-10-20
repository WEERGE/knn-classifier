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


def main():
    data = collect_points()

    total = sum(len(points) for points in data.values())
    labels = set(data.keys())
    print(f"\nВведено {total} точек, метки классов: {', '.join(labels)}")

    print("\nВведите координаты точки неизвестного класса.")
    point = read_point("неизвестной точки")

    k = read_k(total)

    nearest = neighbours(data, point, k)

    print(f"\nБлижайшие соседи точки ({point[0]:.1f}, {point[1]:.1f}):")
    for dist_sq, label, p in nearest:
        print(f"({p[0]:.1f}, {p[1]:.1f})  расстояние {math.sqrt(dist_sq):.2f}  метка {label}")

    predicted = predict(data, point, k)

    votes = {}
    for _, label, _ in nearest:
        votes[label] = votes.get(label, 0) + 1

    votes_str = ", ".join(f"{label} – {count}" for label, count in votes.items())
    print(f"\nГолоса: {votes_str}")
    print(f"Предсказанная метка класса: {predicted}")


if __name__ == '__main__':
    main()