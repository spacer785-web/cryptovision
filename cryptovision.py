import hashlib
import sys
import random

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Не установлены зависимости. Запустите: pip install -r requirements.txt")
    sys.exit(1)


def wallet_fingerprint(address: str, size: int = 9, show: bool = True, save: str = None):
    """
    Генерация уникального визуального отпечатка крипто-адреса.

    :param address: Криптовалютный адрес (строка).
    :param size: Размер матрицы (нечётное число, например 9).
    :param show: Показать рисунок в окне.
    :param save: Сохранить PNG в файл.
    """
    # Хэшируем адрес, чтобы получить стабильный источник "шума"
    digest = hashlib.sha256(address.encode()).hexdigest()

    # Преобразуем в последовательность битов
    bits = bin(int(digest, 16))[2:].zfill(size * size)

    # Генерация матрицы
    matrix = np.array([int(b) for b in bits[: size * size]]).reshape(size, size)

    # Немного "симметрии", чтобы выглядело как иконка
    half = size // 2
    for i in range(size):
        for j in range(half):
            matrix[i][size - 1 - j] = matrix[i][j]

    # Цвет зависит от адреса
    random.seed(int(digest[:8], 16))
    color = (random.random(), random.random(), random.random())

    plt.imshow(matrix, cmap="gray_r")
    plt.axis("off")
    plt.title(f"Wallet fingerprint\n{address[:6]}...{address[-6:]}", fontsize=10, pad=10)
    plt.gca().set_facecolor(color)

    if save:
        plt.savefig(save, bbox_inches="tight", dpi=200)
        print(f"✅ Отпечаток сохранён в {save}")

    if show:
        plt.show()


def main():
    if len(sys.argv) < 2:
        print("Использование: python cryptovision.py <wallet_address> [--save file.png]")
        sys.exit(1)

    address = sys.argv[1]
    save_path = None

    if "--save" in sys.argv:
        idx = sys.argv.index("--save")
        if idx + 1 < len(sys.argv):
            save_path = sys.argv[idx + 1]

    wallet_fingerprint(address, save=save_path)


if __name__ == "__main__":
    main()
