import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Herois.css";

function Herois() {
  const navigate = useNavigate();

  const [herois, setHerois] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const carregarHerois = async () => {
      const token = localStorage.getItem("access_token");

      const response = await fetch(
        "https://hero-management-api.onrender.com/herois",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      console.log("Heróis recebidos:", data);

      setHerois(data);
      setCarregando(false);
    };

    carregarHerois();
  }, []);

  return (
    <main className="herois-page">
      <header className="herois-header">
        <div>
          <span className="herois-badge">HERO MANAGEMENT</span>
          <h1>Gerenciamento de Heróis</h1>
          <p>Consulte e gerencie os heróis da operação.</p>
        </div>

        <button
          className="voltar-button"
          onClick={() => navigate("/dashboard")}
        >
          Voltar
        </button>
      </header>

      <section className="herois-content">
        <div className="herois-title">
          <div>
            <span>HERÓIS CADASTRADOS</span>
            <h2>Equipe operacional</h2>
          </div>

          <button className="novo-heroi-button">
            + Novo herói
          </button>
        </div>

        {carregando ? (
          <div className="herois-empty">
            <h3>Carregando heróis...</h3>
            <p>Aguarde enquanto consultamos a API.</p>
          </div>
        ) : herois.length === 0 ? (
          <div className="herois-empty">
            <h3>Nenhum herói cadastrado</h3>
            <p>
              Ainda não existem heróis cadastrados na operação.
            </p>
          </div>
        ) : (
          <div>
            {herois.map((heroi) => (
              <div key={heroi.id}>
                {heroi.codinome}
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default Herois;