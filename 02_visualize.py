import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config.common import FIGURES, read_splits

train, valid, test = read_splits()
plt.style.use("seaborn-v0_8-whitegrid")

def save_plot(name):
    plt.tight_layout()
    plt.savefig(FIGURES / name, dpi=150)
    plt.close()

plt.figure(figsize=(9, 4))
plt.plot(train.date, train.rentals, label="Qiratë ditore", alpha=0.6)
plt.plot(train.date, train.rentals_mean7, label="Mesatarja e kaluar 7d")
plt.ylabel("Qira / ditë")
plt.title("Kërkesa në periudhën train")
plt.legend()
save_plot("01_demand.png")

train.groupby("workingday").rentals.mean().plot.bar(color="#167d9a")
plt.xticks([0, 1], ["Fundjavë/festë", "Ditë pune"], rotation=0)
plt.ylabel("Qira mesatare / ditë")
plt.title("Mesatarja sipas ditës, vetëm train")
save_plot("02_workingday.png")

plt.scatter(train.temp_c_lag7, train.rentals, alpha=0.5, s=15)
plt.xlabel("Temperatura NASA t−7 (°C)")
plt.ylabel("Qiratë e ditës t")
plt.title("Moti dhe kërkesa, vetëm train")
save_plot("03_weather.png")
print("U krijuan 3 figura te reports/figures/.")
