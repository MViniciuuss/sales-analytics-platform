import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  BarChart3,
  Boxes,
  CircleDollarSign,
  DollarSign,
  LayoutDashboard,
  LogOut,
  Package,
  ReceiptText,
  ShoppingCart,
  TrendingUp,
  Users,
} from "lucide-react";

import { api } from "../services/api";
import "./Dashboard.css";


type DashboardData = {
  total_revenue: number;
  total_profit: number;
  profit_margin: number;
  total_orders: number;
  total_customers: number;
  total_items: number;
  average_ticket: number;
  data_source: string;
};


type DashboardCharts = {
  monthly_sales: {
    month: string;
    revenue: number;
  }[];

  channel_sales: {
    channel: string;
    revenue: number;
  }[];

  category_sales: {
    category: string;
    revenue: number;
  }[];
};


type Order = {
  order_id: string;
  order_date: string;
  sales_channel: string;
  payment_method: string;
  customer_id: string;
  customer_name: string;
  city: string;
  state: string;
};


export default function Dashboard() {
  const navigate = useNavigate();

  const [data, setData] = useState<DashboardData | null>(null);

  const [charts, setCharts] =
    useState<DashboardCharts | null>(null);

  const [orders, setOrders] =
    useState<Order[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  const storedUser = localStorage.getItem("user");

  const user = storedUser
    ? JSON.parse(storedUser)
    : { name: "Usuário" };


  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          dashboardResponse,
          ordersResponse,
          chartsResponse,
        ] = await Promise.all([
          api.get("/api/dashboard"),
          api.get("/api/orders?limit=6&offset=0"),
          api.get("/api/dashboard/charts"),
        ]);

        setData(dashboardResponse.data);

        setOrders(
          ordersResponse.data.data
        );

        setCharts(
          chartsResponse.data
        );

      } catch {
        setError(
          "Não foi possível carregar o dashboard."
        );

      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);


  function handleLogout() {
    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    navigate("/login");
  }


  function formatCurrency(
    value?: number
  ) {
    return new Intl.NumberFormat(
      "pt-BR",
      {
        style: "currency",
        currency: "BRL",
      }
    ).format(value ?? 0);
  }


  function formatNumber(
    value?: number
  ) {
    return new Intl.NumberFormat(
      "pt-BR"
    ).format(value ?? 0);
  }


  function formatDate(
    date: string
  ) {
    return new Intl.DateTimeFormat(
      "pt-BR"
    ).format(
      new Date(
        `${date}T00:00:00`
      )
    );
  }


  function formatCompactCurrency(
    value: number
  ) {
    if (value >= 1_000_000) {
      return `R$ ${(value / 1_000_000).toFixed(1)} mi`;
    }

    if (value >= 1_000) {
      return `R$ ${(value / 1_000).toFixed(1)} mil`;
    }

    return formatCurrency(value);
  }


  if (loading) {
    return (
      <div className="dashboard-loading">
        Carregando dashboard...
      </div>
    );
  }


  if (
    error ||
    !data ||
    !charts
  ) {
    return (
      <div className="dashboard-loading">
        {error ||
          "Erro ao carregar dados."}
      </div>
    );
  }


  return (
    <div className="dashboard-layout">

      <aside className="dashboard-sidebar">

        <div className="sidebar-brand">

          <div className="sidebar-logo">
            <BarChart3 size={22} />
          </div>

          <div>
            <strong>
              Sales Analytics
            </strong>

            <span>
              Data Platform
            </span>
          </div>

        </div>


        <nav className="sidebar-nav">

          <button className="nav-item active">
            <LayoutDashboard size={19} />
            Dashboard
          </button>

          <button className="nav-item">
            <Users size={19} />
            Clientes
          </button>

          <button className="nav-item">
            <Package size={19} />
            Produtos
          </button>

          <button className="nav-item">
            <ShoppingCart size={19} />
            Pedidos
          </button>

        </nav>


        <div className="sidebar-footer">

          <div className="database-status">

            <span className="status-dot" />

            <div>
              <strong>
                PostgreSQL
              </strong>

              <span>
                Conectado
              </span>
            </div>

          </div>


          <button
            className="logout-button"
            onClick={handleLogout}
          >
            <LogOut size={18} />
            Sair
          </button>

        </div>

      </aside>


      <main className="dashboard-main">

        <header className="dashboard-header">

          <div>

            <span className="dashboard-eyebrow">
              VISÃO GERAL
            </span>

            <h1>
              Dashboard
            </h1>

            <p>
              Acompanhe os principais
              indicadores da operação.
            </p>

          </div>


          <div className="user-area">

            <div className="user-avatar">
              {user.name
                ?.charAt(0)
                .toUpperCase()}
            </div>

            <div>

              <strong>
                {user.name}
              </strong>

              <span>
                Administrador
              </span>

            </div>

          </div>

        </header>


        <section className="kpi-grid">

          <article className="kpi-card">

            <div className="kpi-icon">
              <DollarSign size={22} />
            </div>

            <div className="kpi-content">

              <span>
                Faturamento total
              </span>

              <strong>
                {formatCurrency(
                  data.total_revenue
                )}
              </strong>

              <small>
                Receita consolidada
              </small>

            </div>

          </article>


          <article className="kpi-card">

            <div className="kpi-icon">
              <TrendingUp size={22} />
            </div>

            <div className="kpi-content">

              <span>
                Lucro total
              </span>

              <strong>
                {formatCurrency(
                  data.total_profit
                )}
              </strong>

              <small>
                Margem de{" "}
                {data.profit_margin}%
              </small>

            </div>

          </article>


          <article className="kpi-card">

            <div className="kpi-icon">
              <ReceiptText size={22} />
            </div>

            <div className="kpi-content">

              <span>
                Pedidos
              </span>

              <strong>
                {formatNumber(
                  data.total_orders
                )}
              </strong>

              <small>
                Pedidos processados
              </small>

            </div>

          </article>


          <article className="kpi-card">

            <div className="kpi-icon">
              <Users size={22} />
            </div>

            <div className="kpi-content">

              <span>
                Clientes
              </span>

              <strong>
                {formatNumber(
                  data.total_customers
                )}
              </strong>

              <small>
                Clientes únicos
              </small>

            </div>

          </article>

        </section>


        <section className="secondary-kpis">

          <article>

            <CircleDollarSign size={20} />

            <div>

              <span>
                Ticket médio
              </span>

              <strong>
                {formatCurrency(
                  data.average_ticket
                )}
              </strong>

            </div>

          </article>


          <article>

            <Boxes size={20} />

            <div>

              <span>
                Itens vendidos
              </span>

              <strong>
                {formatNumber(
                  data.total_items
                )}
              </strong>

            </div>

          </article>


          <article>

            <TrendingUp size={20} />

            <div>

              <span>
                Margem
              </span>

              <strong>
                {data.profit_margin}%
              </strong>

            </div>

          </article>

        </section>


        <section className="charts-grid">

          <article className="chart-card chart-large">

            <div className="chart-header">

              <div>

                <h2>
                  Evolução do faturamento
                </h2>

                <p>
                  Receita mensal entre
                  2023 e 2025.
                </p>

              </div>

            </div>


            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <LineChart
                  data={
                    charts.monthly_sales
                  }
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                    stroke="#edf0f5"
                  />

                  <XAxis
                    dataKey="month"
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                    minTickGap={30}
                  />

                  <YAxis
                    tickFormatter={
                      formatCompactCurrency
                    }
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                    width={80}
                  />

                  <Tooltip
                    formatter={(value) =>
                      formatCurrency(
                        Number(value)
                      )
                    }
                  />

                  <Line
                    type="monotone"
                    dataKey="revenue"
                    stroke="#2563eb"
                    strokeWidth={3}
                    dot={false}
                  />

                </LineChart>

              </ResponsiveContainer>

            </div>

          </article>


          <article className="chart-card">

            <div className="chart-header">

              <div>

                <h2>
                  Vendas por canal
                </h2>

                <p>
                  Distribuição do
                  faturamento.
                </p>

              </div>

            </div>


            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart
                  data={
                    charts.channel_sales
                  }
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                    stroke="#edf0f5"
                  />

                  <XAxis
                    dataKey="channel"
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                  />

                  <YAxis
                    tickFormatter={
                      formatCompactCurrency
                    }
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                    width={75}
                  />

                  <Tooltip
                    formatter={(value) =>
                      formatCurrency(
                        Number(value)
                      )
                    }
                  />

                  <Bar
                    dataKey="revenue"
                    fill="#2563eb"
                    radius={[
                      6,
                      6,
                      0,
                      0,
                    ]}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </article>


          <article className="chart-card">

            <div className="chart-header">

              <div>

                <h2>
                  Faturamento por categoria
                </h2>

                <p>
                  Participação das
                  linhas de produto.
                </p>

              </div>

            </div>


            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart
                  data={
                    charts.category_sales
                  }
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                    stroke="#edf0f5"
                  />

                  <XAxis
                    dataKey="category"
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                  />

                  <YAxis
                    tickFormatter={
                      formatCompactCurrency
                    }
                    tick={{
                      fontSize: 10,
                    }}
                    axisLine={false}
                    tickLine={false}
                    width={75}
                  />

                  <Tooltip
                    formatter={(value) =>
                      formatCurrency(
                        Number(value)
                      )
                    }
                  />

                  <Bar
                    dataKey="revenue"
                    fill="#0f172a"
                    radius={[
                      6,
                      6,
                      0,
                      0,
                    ]}
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </article>

        </section>


        <section className="dashboard-panel">

          <div className="panel-header">

            <div>

              <h2>
                Pedidos recentes
              </h2>

              <p>
                Últimas movimentações
                registradas no sistema.
              </p>

            </div>


            <button className="outline-button">
              Ver todos
            </button>

          </div>


          <div className="table-wrapper">

            <table>

              <thead>

                <tr>
                  <th>Pedido</th>
                  <th>Cliente</th>
                  <th>Data</th>
                  <th>Canal</th>
                  <th>Pagamento</th>
                  <th>Localização</th>
                </tr>

              </thead>


              <tbody>

                {orders.map(
                  (order) => (

                    <tr
                      key={
                        order.order_id
                      }
                    >

                      <td className="order-id">
                        #{order.order_id}
                      </td>

                      <td>
                        {
                          order.customer_name
                        }
                      </td>

                      <td>
                        {formatDate(
                          order.order_date
                        )}
                      </td>

                      <td>
                        <span className="table-badge">
                          {
                            order.sales_channel
                          }
                        </span>
                      </td>

                      <td>
                        {
                          order.payment_method
                        }
                      </td>

                      <td>
                        {order.city} -{" "}
                        {order.state}
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        </section>

      </main>

    </div>
  );
}