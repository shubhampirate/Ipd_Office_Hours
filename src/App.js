import { useState } from "react";
import { Routes, Route , useLocation} from "react-router-dom";
import { Outlet, Navigate } from "react-router-dom";
import Topbar from "./scenes/global/Topbar";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import Team from "./scenes/team";
import Invoices from "./scenes/invoices";
import Contacts from "./scenes/contacts";
import Bar from "./scenes/bar";
import Form from "./scenes/form";
import Line from "./scenes/line";
import Pie from "./scenes/pie";
import FAQ from "./scenes/faq";
import Geography from "./scenes/geography";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import Calendar from "./scenes/calendar/calendar";
import Login from "./scenes/login/login";
import Logout from "./scenes/login/logout";
import ProfilePage from "./scenes/profile/profile";

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const location = useLocation();

  const PrivateRoute = () => {
		const token = localStorage.getItem('token')
		return token ? <Outlet /> : <Navigate to="/login" />
	}

  const showSidebar = location.pathname !== "/login";
  console.log(localStorage.getItem('token'));

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          {showSidebar && <Sidebar isSidebar={isSidebar} />}
          <main className="content">
             <Topbar setIsSidebar={setIsSidebar} />
            <Routes>
              <Route path='/' element={<PrivateRoute />} > <Route path="/" element={<Dashboard />} /> </Route>
              <Route exact path='/login' element={<Login />} />
              <Route path="/profile" element={<PrivateRoute />} ><Route path="/profile" element={<ProfilePage />} /> </Route>
              <Route path='/team' element={<PrivateRoute />} ><Route path="/team" element={<Team />} /> </Route>
              <Route path="/notifications_old" element={<PrivateRoute />} ><Route path="/notifications_old" element={<Contacts />} /> </Route>
              <Route path="/invoices" element={<PrivateRoute />} ><Route path="/invoices" element={<Invoices />} /> </Route>
              <Route path="/form" element={<PrivateRoute />} ><Route path="/form" element={<Form />} /> </Route>
              <Route path="/bar" element={<PrivateRoute />} ><Route path="/bar" element={<Bar />} /> </Route>
              <Route path="/pie" element={<PrivateRoute />} ><Route path="/pie" element={<Pie />} /> </Route>
              <Route path="/line" element={<PrivateRoute />} ><Route path="/line" element={<Line />} /> </Route>
              <Route path="/notifications" element={<PrivateRoute />} ><Route path="/notifications" element={<FAQ />} /> </Route>
              <Route path="/calendar" element={<PrivateRoute />} ><Route path="/calendar" element={<Calendar />} /> </Route>
              <Route path="/geography" element={<PrivateRoute />} ><Route path="/geography" element={<Geography />} /> </Route>
              <Route path="/logout" element={<PrivateRoute />} ><Route path="/logout" element={<Logout />} /> </Route>
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
