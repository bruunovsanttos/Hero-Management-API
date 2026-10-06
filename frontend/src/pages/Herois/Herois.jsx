import { useNavigate } from "react-router-dom";
import "./Herois.css";

function Herois() {
  const navigate = useNavigate();

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

        <div className="herois-empty">
          <h3>Nenhum herói carregado</h3>
          <p>
            Os dados da API serão integrados na próxima etapa.
          </p>
        </div>
      </section>
    </main>
  );
}

export default Herois;