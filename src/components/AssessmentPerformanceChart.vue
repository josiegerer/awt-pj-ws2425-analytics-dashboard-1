<template>
    <div class="assessment-performance-chart">
      <h3>Assessment Performance Over Time</h3>
      <LineChart :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';

// Registriere die Chart.js-Komponenten
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement);

export default {
  name: 'AssessmentPointsChart',
  components: {
    LineChart: Line
  },
  data() {
    const now = new Date();
    const currentDay = now.getDate(); // Aktueller Tag im Monat

    // Definiere das maximale Datum, das angezeigt werden soll (z. B. nur bis zum 20. Tag)
    const maxDays = Math.min(currentDay, 20); 

    // Erzeuge eine Liste der Tage 1 - maxDays
    const dayLabels = Array.from({ length: maxDays }, (_, i) => i + 1);

    // Beispielhafte Punktedaten für die Tage 1 - maxDays (dies könnte mit echten Daten ersetzt werden)
    const randomData = dayLabels.map(() => Math.floor(Math.random() * 100)); 

    // Berechne den Durchschnittswert
    const averageValue = randomData.reduce((acc, val) => acc + val, 0) / randomData.length;
    const averageData = Array(maxDays).fill(averageValue); // Konstante Linie für den Durchschnitt

    return {
      chartData: {
        labels: dayLabels, // X-Achse zeigt die Tage bis zum aktuellen Tag oder max 20 Tage
        datasets: [
          {
            label: 'Punkte erreicht',
            data: randomData, // Tageswerte
            borderColor: '#42A5F5',
            backgroundColor: 'rgba(66, 165, 245, 0.2)',
            fill: true,
            tension: 0.4
          },
          {
            label: 'Durchschnitt',
            data: averageData, // Durchschnittswerte für eine horizontale Linie
            borderColor: 'red',
            borderWidth: 2,
            borderDash: [5, 5], // Gepunktete Linie für Durchschnitt
            pointRadius: 0, // Keine Punkte für diese Linie
            fill: false
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return `Punkte: ${context.raw}`;
              }
            }
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: '#000',
              font: { size: 12 }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Tage im Monat'
            },
            ticks: {
              autoSkip: true, // Automatische Reduzierung der Labels, wenn zu viele vorhanden sind
              maxTicksLimit: 10 // Maximal 10 Labels auf der Achse
            }
          },
          y: {
            title: {
              display: true,
              text: 'Assessment Punkte'
            },
            beginAtZero: true,
            min: 0,
            max: 100
          }
        }
      }
    };
  }
};
</script>


  <style scoped>
  h3 {
    text-align: left;
    font-size: 15px;
    color: black;
    margin-bottom: 20px;
  }
  </style>
  