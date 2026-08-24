import { useNavigate } from "react-router-dom";
import { useState, type FormEvent } from "react";
import {
  BarChart3,
  Eye,
  EyeOff,
  Lock,
  Mail,
} from "lucide-react";

import { api } from "../services/api";


export default function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const response = await api.post("/api/auth/login", {
        email,
        password,
      });

      const token = response.data.access_token;
      const user = response.data.user;

      localStorage.setItem("access_token", token);
      localStorage.setItem("user", JSON.stringify(user));

      navigate("/dashboard");

    } catch {
      setError("E-mail ou senha inválidos.");

    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="login-page">
      <section className="login-brand">
        <div className="brand-content">
          <div className="brand-logo">
            <BarChart3 size={30} />
          </div>

          <h1>Sales Analytics</h1>

          <p>
            Transforme dados de vendas em decisões estratégicas.
          </p>

          <div className="brand-stats">
            <div>
              <strong>100k+</strong>
              <span>pedidos analisados</span>
            </div>

            <div>
              <strong>15k</strong>
              <span>clientes</span>
            </div>
          </div>
        </div>
      </section>

      <section className="login-area">
        <div className="login-card">
          <div className="login-header">
            <span className="login-label">
              PLATAFORMA ANALYTICS
            </span>

            <h2>Bem-vindo de volta</h2>

            <p>
              Entre na sua conta para acessar o dashboard.
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            <label>
              E-mail

              <div className="input-wrapper">
                <Mail size={19} />

                <input
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  required
                />
              </div>
            </label>

            <label>
              Senha

              <div className="input-wrapper">
                <Lock size={19} />

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Digite sua senha"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  required
                />

                <button
                  type="button"
                  className="password-button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? (
                    <EyeOff size={19} />
                  ) : (
                    <Eye size={19} />
                  )}
                </button>
              </div>
            </label>

            <div className="login-options">
              <label className="remember">
                <input type="checkbox" />
                Lembrar de mim
              </label>

              <button
                type="button"
                className="forgot-password"
              >
                Esqueci minha senha
              </button>
            </div>

            {error && (
              <p className="login-error">
                {error}
              </p>
            )}

            <button
              type="submit"
              className="login-button"
              disabled={loading}
            >
              {loading
                ? "Entrando..."
                : "Entrar na plataforma"}
            </button>
          </form>

          <p className="login-footer">
            Sales Analytics Platform • Full Stack Data Solution
          </p>
        </div>
      </section>
    </main>
  );
}