async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  if (!response.ok) {
    let detail = `HTTP ${response.status}`
    try {
      const data = await response.json()
      if (typeof data?.detail === 'string') detail = data.detail
    } catch {
      // ignore
    }
    throw new Error(detail)
  }

  if (response.status === 204) return null
  return response.json()
}

export function getTasks() {
  return request('/api/tasks')
}

export function getTask(id) {
  return request(`/api/tasks/${id}`)
}

export function createTask(payload) {
  return request('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateTask(id, payload) {
  return request(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteTask(id) {
  return request(`/api/tasks/${id}`, {
    method: 'DELETE',
  })
}
