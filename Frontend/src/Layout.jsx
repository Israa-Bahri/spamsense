// Import the CSS file that styles this component
import "./Layout.css";

// A component is a function that returns JSX.
// { children } = whatever is placed between <Layout> and </Layout>
export default function Layout({ children }) {
  return (
    <div className="layout">
      <header>SpamSense</header>

      {/* children is replaced by the page content from App.jsx */}
      <main>{children}</main>

      <footer>© 2026</footer>
    </div>
  );
}