// This script assumes that the backend APIs are running on localhost:5000
// and the frontend is running on localhost:3000.

// Function to delete an investor
async function deleteInvestor(id) {
    const confirmDelete = confirm('Are you sure you want to delete this investor?');
    if (confirmDelete) {
      try {
        const response = await fetch(`http://localhost:5000/api/investors/${id}`, {
          method: 'DELETE',
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.Message);
          location.reload(); // Reload the page to update the list
        } else {
          alert(data.Error || 'Failed to delete investor.');
        }
      } catch (error) {
        console.error('Error deleting investor:', error);
        alert('An error occurred while deleting the investor.');
      }
    }
  }
  
  // Function to delete a stock
  async function deleteStock(id) {
    const confirmDelete = confirm('Are you sure you want to delete this stock?');
    if (confirmDelete) {
      try {
        const response = await fetch(`http://localhost:5000/api/stocks/${id}`, {
          method: 'DELETE',
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.Message);
          location.reload(); // Reload the page to update the list
        } else {
          alert(data.Error || 'Failed to delete stock.');
        }
      } catch (error) {
        console.error('Error deleting stock:', error);
        alert('An error occurred while deleting the stock.');
      }
    }
  }
  
  // Function to delete a bond
  async function deleteBond(id) {
    const confirmDelete = confirm('Are you sure you want to delete this bond?');
    if (confirmDelete) {
      try {
        const response = await fetch(`http://localhost:5000/api/bonds/${id}`, {
          method: 'DELETE',
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.Message);
          location.reload(); // Reload the page to update the list
        } else {
          alert(data.Error || 'Failed to delete bond.');
        }
      } catch (error) {
        console.error('Error deleting bond:', error);
        alert('An error occurred while deleting the bond.');
      }
    }
  }
  
  // Function to load portfolio details dynamically
  async function loadPortfolio(investorId) {
    try {
      const response = await fetch(`http://localhost:5000/api/investor/${investorId}/portfolio`);
      const portfolio = await response.json();
      if (response.ok) {
        // Render portfolio details dynamically
        const portfolioContainer = document.getElementById('portfolio-container');
        portfolioContainer.innerHTML = `
          <h2>Stocks</h2>
          <ul>
            ${portfolio.stocks
              .map(stock => `<li>${stock.stockname}: ${stock.quantity}</li>`)
              .join('')}
          </ul>
          <h2>Bonds</h2>
          <ul>
            ${portfolio.bonds
              .map(bond => `<li>${bond.bondname}: ${bond.quantity}</li>`)
              .join('')}
          </ul>
        `;
      } else {
        alert(portfolio.Error || 'Failed to load portfolio.');
      }
    } catch (error) {
      console.error('Error loading portfolio:', error);
      alert('An error occurred while loading the portfolio.');
    }
  }
  
  // Function to handle form submissions (Add/Edit)
  async function submitForm(event, url, method) {
    event.preventDefault(); // Prevent form submission
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
  
    try {
      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const result = await response.json();
      if (response.ok) {
        alert(result.message || 'Operation successful.');
        location.reload(); // Reload the page to reflect changes
      } else {
        alert(result.Error || 'Operation failed.');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('An error occurred while processing the form.');
    }
  }
  
  // Attach form submission handlers dynamically (Example for investor form)
  document.addEventListener('DOMContentLoaded', () => {
    const investorForm = document.getElementById('investor-form');
    if (investorForm) {
      investorForm.addEventListener('submit', (e) =>
        submitForm(e, 'http://localhost:5000/api/investors', 'POST')
      );
    }
  });
