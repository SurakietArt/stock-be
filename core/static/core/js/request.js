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
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    'X-CSRFToken': getCSRFToken()
  };

  const options = {
    method: method.toUpperCase(),
    headers,
    credentials: 'include',
    ...(body && { body: JSON.stringify(body) })
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
    if (err.message === 'Unauthorized' || err.message === 'Token is invalid') {
      console.log('🔄 Access token expired. Trying refresh...');
      const refreshRes = await fetch('/api/v1/token/refresh/', {
        method: 'POST',
        credentials: 'include'
      });

      if (refreshRes.ok) {
        const data = await refreshRes.json();
        localStorage.setItem('access_token', data.access);
        return await window.apiRequest(url, method, body);
      } else {
        throw new Error('Refresh token failed');
      }
    }

    throw err;
  }
};
