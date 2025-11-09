import { 
  BrowserRouter as Router, 
  Routes, 
  Route, 
  Navigate 
} from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext.jsx';
import PrivateRoute from './auth/PrivateRouter.jsx';
import Login from './auth/login.jsx';
import Register from './auth/Register.jsx';
import Dashboard from './components/Dashboard.jsx';
import MisReservas from './components/MisReservas.jsx';

function App() {
  return (
    <AuthProvider> 
      <Router> 
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route 
            path="/dashboard" 
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/mis-reservas" 
            element={ 
            <PrivateRoute>
               <MisReservas />
            </PrivateRoute> 
            } 
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;