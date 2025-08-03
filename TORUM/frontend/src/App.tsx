import { Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Posts from './pages/Post';
import ViewPost from './pages/PostView';
import AccountManagement from './pages/AccountManagement';
import UploadDocument from './pages/UploadDocument';
import DocumentList from './pages/DocumentList';
import Search from './pages/Search';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/search" element={<Search />} />
        <Route 
          path="/post" 
          element={
            <ProtectedRoute>
              <Posts />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/view-post"
          element={
            <ProtectedRoute>
              <ViewPost />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/account"
          element={
            <ProtectedRoute>
              <AccountManagement />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/view-document"
          element={
            <ProtectedRoute>
              <DocumentList />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/upload-document"
          element={
            <ProtectedRoute>
              <UploadDocument />
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  );
}

export default App;