const API = "https://prathibha-lms-backend.onrender.com";

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "API error");
  }
  return res.json();
}

const db = {
  teachers: {
    async find(criteria = {}) {
      const all = await apiFetch("/api/teachers/");
      return all.filter(t => matchesCriteria(t, criteria));
    },
    async findOne(criteria = {}) {
      const all = await this.find(criteria);
      return all[0] || null;
    },
    async insertOne(doc) {
      return apiFetch("/api/teachers/", { method: "POST", body: JSON.stringify(doc) });
    },
    async updateOne(criteria, updates) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/teachers/${item.id}`, { method: "PUT", body: JSON.stringify(updates) });
      return 1;
    },
    async deleteOne(criteria) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/teachers/${item.id}`, { method: "DELETE" });
      return 1;
    }
  },

  students: {
    async find(criteria = {}) {
      const all = await apiFetch("/api/students/");
      return all.filter(s => matchesCriteria(s, criteria));
    },
    async findOne(criteria = {}) {
      const all = await this.find(criteria);
      return all[0] || null;
    },
    async insertOne(doc) {
      return apiFetch("/api/students/", { method: "POST", body: JSON.stringify(doc) });
    },
    async updateOne(criteria, updates) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/students/${item.id}`, { method: "PUT", body: JSON.stringify(updates) });
      return 1;
    },
    async deleteOne(criteria) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/students/${item.id}`, { method: "DELETE" });
      return 1;
    }
  },

  quizzes: {
    async find(criteria = {}) {
      const all = await apiFetch("/api/quizzes/");
      return all.filter(q => matchesCriteria(q, criteria));
    },
    async findOne(criteria = {}) {
      const all = await this.find(criteria);
      return all[0] || null;
    },
    async insertOne(doc) {
      return apiFetch("/api/quizzes/", { method: "POST", body: JSON.stringify(doc) });
    },
    async updateOne(criteria, updates) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/quizzes/${item.id}`, { method: "PUT", body: JSON.stringify(updates) });
      return 1;
    },
    async deleteOne(criteria) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/quizzes/${item.id}`, { method: "DELETE" });
      return 1;
    }
  },

  announcements: {
    async find(criteria = {}) {
      const all = await apiFetch("/api/announcements/");
      return all.filter(a => matchesCriteria(a, criteria));
    },
    async findOne(criteria = {}) {
      const all = await this.find(criteria);
      return all[0] || null;
    },
    async insertOne(doc) {
      return apiFetch("/api/announcements/", { method: "POST", body: JSON.stringify(doc) });
    },
    async updateOne(criteria, updates) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/announcements/${item.id}`, { method: "PUT", body: JSON.stringify(updates) });
      return 1;
    },
    async deleteOne(criteria) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/announcements/${item.id}`, { method: "DELETE" });
      return 1;
    }
  },

  feedback: {
    async find(criteria = {}) {
      const all = await apiFetch("/api/feedback/");
      return all.filter(f => matchesCriteria(f, criteria));
    },
    async findOne(criteria = {}) {
      const all = await this.find(criteria);
      return all[0] || null;
    },
    async insertOne(doc) {
      return apiFetch("/api/feedback/", { method: "POST", body: JSON.stringify(doc) });
    },
    async deleteOne(criteria) {
      const item = await this.findOne(criteria);
      if (!item) return 0;
      await apiFetch(`/api/feedback/${item.id}`, { method: "DELETE" });
      return 1;
    }
  },

  settings: {
    async get() {
      return apiFetch("/api/settings/");
    },
    async update(updates) {
      return apiFetch("/api/settings/", { method: "PUT", body: JSON.stringify(updates) });
    },
    async incrementVisitor() {
      const current = await this.get();
      const newCount = (current.visitorCount || 0) + 1;
      await this.update({ visitorCount: newCount });
      return newCount;
    }
  }
};

function matchesCriteria(item, criteria) {
  for (let key in criteria) {
    if (Array.isArray(item[key])) {
      if (!item[key].includes(criteria[key])) return false;
    } else if (item[key] !== criteria[key]) return false;
  }
  return true;
}

window.db = db;