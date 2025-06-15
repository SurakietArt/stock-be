function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

window.apiRequest = async function(url, method = 'GET', body = null) {
  const token = localStorage.getItem('access_token');

  const isFormData = body instanceof URLSearchParams;

  const headers = {
    ...(token && { 'Authorization': `Bearer ${token}` }),
    'X-CSRFToken': getCSRFToken(),
    ...(isFormData
      ? { 'Content-Type': 'application/x-www-form-urlencoded' }
      : { 'Content-Type': 'application/json' }
    )
  };

  const options = {
    method: method.toUpperCase(),
    headers,
    credentials: 'include',
    ...(body && { body: isFormData ? body.toString() : JSON.stringify(body) })
  };

  try {
    const response = await fetch(url, options);
    const contentType = response.headers.get('content-type');

    const data = contentType?.includes('application/json')
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      throw new Error(data?.detail ?? 'API Error');
    }

    return data;
  } catch (err) {
    console.error('API request failed:', err);
    throw err;
  }
};

window.apiRequestWithRefresh = async function (url, method = 'GET', body = null) {
  try {
    return await window.apiRequest(url, method, body);
  } catch (err) {
    if (err.message === 'Token Expire') {
      const refreshRes = await fetch('/api/v1/refresh', {
        method: 'POST',
        credentials: 'include'
      });

      const data = await refreshRes.json();
      if (refreshRes.ok) {
        localStorage.setItem('access_token', data.access);
        return await window.apiRequest(url, method, body);
      } else if (data.login_url) {
        window.location.href = data.login_url;
      } else {
        throw new Error('Refresh token failed and no login URL provided');
      }
    }
            throw err;
  }
};
