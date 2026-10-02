import "./Dashboard.css";

function Dashboard() {
  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <span className="dashboard-badge">HERO MANAGEMENT</span>
          <h1>Central de Operações</h1>
          <p>Gerencie heróis, ameaças e missões em um só lugar.</p>
        </div>

        <button className="logout-button">
          Sair
        </button>
      </header>

      <section className="dashboard-content">
        <div className="dashboard-welcome">
          <div>
            <span>PAINEL OPERACIONAL</span>
            <h2>Visão geral</h2>
          </div>

          <p>Acompanhe e gerencie os recursos da operação.</p>
        </div>

        <div className="dashboard-cards">
          <article className="dashboard-card">
            <div className="card-number">01</div>

            <div>
              <h3>Heróis</h3>
              <p>
                Consulte e gerencie os heróis cadastrados na operação.
              </p>
            </div>

            <button>Gerenciar heróis</button>
          </article>

          <article className="dashboard-card">
            <div className="card-number">02</div>

            <div>
              <h3>Ameaças</h3>
              <p>
                Visualize as ameaças registradas e seus respectivos status.
              </p>
            </div>

            <button>Gerenciar ameaças</button>
          </article>

          <article className="dashboard-card">
            <div className="card-number">03</div>

            <div>
              <h3>Missões</h3>
              <p>
                Acompanhe as missões e o andamento das operações.
              </p>
            </div>

            <button>Gerenciar missões</button>
          </article>
        </div>
      </section>
    </main>
  );
}

export default Dashboard;