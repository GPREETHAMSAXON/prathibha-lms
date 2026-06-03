const SESSION_KEY = "prathibha_session";

const auth = {
  async login(email, password) {
    try {
      const res = await fetch("https://prathibha-lms-backend.onrender.com/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        localStorage.setItem(SESSION_KEY, JSON.stringify({ user: data.user }));
        return { success: true, user: data.user };
      }
      return { success: false, message: data.detail || "Invalid email or password" };
    } catch (e) {
      return { success: false, message: "Cannot connect to server. Please try again." };
    }
  },

  logout() {
    localStorage.removeItem(SESSION_KEY);
    return true;
  },

  getCurrentUser() {
    const sessionData = localStorage.getItem(SESSION_KEY);
    if (!sessionData) return null;
    try {
      const session = JSON.parse(sessionData);
      return session.user;
    } catch (e) {
      this.logout();
      return null;
    }
  },

  isAuthenticated() {
    return this.getCurrentUser() !== null;
  },

  isPrincipal() {
    const user = this.getCurrentUser();
    return user && user.role === "principal";
  },

  isTeacher() {
    const user = this.getCurrentUser();
    return user && user.role === "teacher";
  },

  isStudent() {
    const user = this.getCurrentUser();
    return user && user.role === "student";
  }
};

window.auth = auth;