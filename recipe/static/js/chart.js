// Function to generate kundali chart
function generateKundaliChart(kundaliData) {
    const chartContainer = document.getElementById('kundali-chart');
    if (!chartContainer) return;
    
    // Clear previous chart
    chartContainer.innerHTML = '';
    
    // Create 12 houses in circular pattern
    const houses = [
        { number: 1, name: "Lagna", planets: [] },
        { number: 2, name: "Dhana", planets: [] },
        { number: 3, name: "Sahaja", planets: [] },
        { number: 4, name: "Sukha", planets: [] },
        { number: 5, name: "Putra", planets: [] },
        { number: 6, name: "Ripu", planets: [] },
        { number: 7, name: "Kalatra", planets: [] },
        { number: 8, name: "Ayush", planets: [] },
        { number: 9, name: "Bhagya", planets: [] },
        { number: 10, name: "Karma", planets: [] },
        { number: 11, name: "Labha", planets: [] },
        { number: 12, name: "Vyaya", planets: [] }
    ];
    
    // Assign planets to houses based on their positions
    Object.entries(kundaliData.planetary_positions).forEach(([planet, rasi]) => {
        const rasiIndex = Object.keys(kundaliData.rasi_names).indexOf(rasi);
        if (rasiIndex !== -1) {
            const houseIndex = rasiIndex % 12;
            houses[houseIndex].planets.push(planet);
        }
    });
    
    // Special case - Lagna house should show Lagna sign
    houses[0].planets.unshift(`Lagna: ${kundaliData.lagna}`);
    
    // Create SVG container
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 400 400");
    svg.setAttribute("class", "kundali-svg");
    
    // Draw outer circle
    const outerCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    outerCircle.setAttribute("cx", "200");
    outerCircle.setAttribute("cy", "200");
    outerCircle.setAttribute("r", "180");
    outerCircle.setAttribute("fill", "none");
    outerCircle.setAttribute("stroke", "#6c5ce7");
    outerCircle.setAttribute("stroke-width", "2");
    svg.appendChild(outerCircle);
    
    // Draw inner circle
    const innerCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    innerCircle.setAttribute("cx", "200");
    innerCircle.setAttribute("cy", "200");
    innerCircle.setAttribute("r", "120");
    innerCircle.setAttribute("fill", "none");
    innerCircle.setAttribute("stroke", "#a29bfe");
    innerCircle.setAttribute("stroke-width", "1");
    svg.appendChild(innerCircle);
    
    // Draw house divisions
    for (let i = 0; i < 12; i++) {
        const angle = (i * 30) * Math.PI / 180;
        
        // Draw division line
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", "200");
        line.setAttribute("y1", "200");
        line.setAttribute("x2", "200 + 180 * Math.cos(angle)");
        line.setAttribute("y2", "200 + 180 * Math.sin(angle)");
        line.setAttribute("stroke", "#dfe6e9");
        line.setAttribute("stroke-width", "1");
        svg.appendChild(line);
        
        // Calculate house label position
        const labelAngle = (i * 30 + 15) * Math.PI / 180;
        const labelX = 200 + 150 * Math.cos(labelAngle);
        const labelY = 200 + 150 * Math.sin(labelAngle);
        
        // Create house label
        const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", labelX);
        label.setAttribute("y", labelY);
        label.setAttribute("text-anchor", "middle");
        label.setAttribute("fill", "#6c5ce7");
        label.setAttribute("font-size", "14");
        label.textContent = houses[i].number;
        svg.appendChild(label);
        
        // Create house content group
        const contentGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        contentGroup.setAttribute("transform", `translate(${labelX}, ${labelY + 20})`);
        
        // Add house name
        const houseName = document.createElementNS("http://www.w3.org/2000/svg", "text");
        houseName.setAttribute("text-anchor", "middle");
        houseName.setAttribute("fill", "#2d3436");
        houseName.setAttribute("font-size", "10");
        houseName.textContent = houses[i].name;
        contentGroup.appendChild(houseName);
        
        // Add planets in house
        houses[i].planets.forEach((planet, idx) => {
            const planetText = document.createElementNS("http://www.w3.org/2000/svg", "text");
            planetText.setAttribute("text-anchor", "middle");
            planetText.setAttribute("fill", "#00b894");
            planetText.setAttribute("font-size", "9");
            planetText.setAttribute("y", 15 + idx * 12);
            planetText.textContent = planet;
            contentGroup.appendChild(planetText);
        });
        
        svg.appendChild(contentGroup);
    }
    
    // Add Nakshatra info at center
    const centerGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    centerGroup.setAttribute("transform", "translate(200, 200)");
    
    const nakshatraText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    nakshatraText.setAttribute("text-anchor", "middle");
    nakshatraText.setAttribute("fill", "#d63031");
    nakshatraText.setAttribute("font-size", "12");
    nakshatraText.setAttribute("y", "-10");
    nakshatraText.textContent = `Nakshatra: ${kundaliData.nakshatra}`;
    centerGroup.appendChild(nakshatraText);
    
    const tithiText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    tithiText.setAttribute("text-anchor", "middle");
    tithiText.setAttribute("fill", "#2d3436");
    tithiText.setAttribute("font-size", "10");
    tithiText.setAttribute("y", "10");
    tithiText.textContent = `Tithi: ${kundaliData.tithi}`;
    centerGroup.appendChild(tithiText);
    
    svg.appendChild(centerGroup);
    
    // Add SVG to container
    chartContainer.appendChild(svg);
}

// Function to generate western astrology chart
function generateWesternChart(signData) {
    // Similar implementation for western astrology chart
    // Would show planets in signs and aspects between them
}

// Function to generate compatibility chart
function generateCompatibilityChart(compatibilityData) {
    const container = document.getElementById('compatibility-chart');
    if (!container) return;
    
    container.innerHTML = '';
    
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 400 300");
    svg.setAttribute("class", "compatibility-svg");
    
    // Create meter bars for each compatibility aspect
    const aspects = [
        { name: 'Love', value: compatibilityData.compatibility.love },
        { name: 'Trust', value: compatibilityData.compatibility.trust },
        { name: 'Communication', value: compatibilityData.compatibility.communication },
        { name: 'Friendship', value: compatibilityData.compatibility.friendship },
        { name: 'Marriage', value: compatibilityData.compatibility.marriage }
    ];
    
    aspects.forEach((aspect, index) => {
        const yPos = 30 + index * 50;
        
        // Aspect name
        const nameText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        nameText.setAttribute("x", "20");
        nameText.setAttribute("y", yPos);
        nameText.setAttribute("fill", "#2d3436");
        nameText.textContent = aspect.name;
        svg.appendChild(nameText);
        
        // Meter background
        const bgRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        bgRect.setAttribute("x", "150");
        bgRect.setAttribute("y", yPos - 15);
        bgRect.setAttribute("width", "200");
        bgRect.setAttribute("height", "20");
        bgRect.setAttribute("fill", "#dfe6e9");
        svg.appendChild(bgRect);
        
        // Meter fill
        const fillRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        fillRect.setAttribute("x", "150");
        fillRect.setAttribute("y", yPos - 15);
        fillRect.setAttribute("width", `${aspect.value * 2}`);
        fillRect.setAttribute("height", "20");
        fillRect.setAttribute("fill", getCompatibilityColor(aspect.value));
        svg.appendChild(fillRect);
        
        // Percentage text
        const percentText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        percentText.setAttribute("x", "360");
        percentText.setAttribute("y", yPos);
        percentText.setAttribute("fill", "#2d3436");
        percentText.textContent = `${aspect.value}%`;
        svg.appendChild(percentText);
    });
    
    // Add pros and cons
    const prosConsGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    prosConsGroup.setAttribute("transform", "translate(20, 280)");
    
    const prosText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    prosText.setAttribute("x", "0");
    prosText.setAttribute("y", "0");
    prosText.setAttribute("font-weight", "bold");
    prosText.setAttribute("fill", "#00b894");
    prosText.textContent = "Pros:";
    prosConsGroup.appendChild(prosText);
    
    const prosContent = document.createElementNS("http://www.w3.org/2000/svg", "text");
    prosContent.setAttribute("x", "50");
    prosContent.setAttribute("y", "0");
    prosContent.setAttribute("fill", "#2d3436");
    prosContent.textContent = compatibilityData.pros;
    prosConsGroup.appendChild(prosContent);
    
    const consText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    consText.setAttribute("x", "0");
    consText.setAttribute("y", "20");
    consText.setAttribute("font-weight", "bold");
    consText.setAttribute("fill", "#d63031");
    consText.textContent = "Cons:";
    prosConsGroup.appendChild(consText);
    
    const consContent = document.createElementNS("http://www.w3.org/2000/svg", "text");
    consContent.setAttribute("x", "50");
    consContent.setAttribute("y", "20");
    consContent.setAttribute("fill", "#2d3436");
    consContent.textContent = compatibilityData.cons;
    prosConsGroup.appendChild(consContent);
    
    svg.appendChild(prosConsGroup);
    
    container.appendChild(svg);
}

function getCompatibilityColor(value) {
    if (value < 30) return "#d63031"; // Red
    if (value < 60) return "#fdcb6e"; // Yellow
    if (value < 80) return "#00b894"; // Green
    return "#6c5ce7"; // Purple for high values
}

// Initialize all charts on page load
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('kundali-chart')) {
        // This would be replaced with actual data from the server
        const sampleKundali = {
            lagna: "Mesha",
            nakshatra: "Rohini",
            planetary_positions: {
                "Sun": "Simha",
                "Moon": "Karka",
                "Mars": "Mesha",
                "Mercury": "Kanya",
                "Jupiter": "Dhanu",
                "Venus": "Tula",
                "Saturn": "Makara",
                "Rahu": "Vrishabha",
                "Ketu": "Vrishchika"
            },
            tithi: "Shukla Paksha Dashami",
            yoga: "Siddha",
            karana: "Bava"
        };
        generateKundaliChart(sampleKundali);
    }
    
    if (document.getElementById('compatibility-chart')) {
        const sampleCompatibility = {
            compatibility: {
                love: 85,
                trust: 72,
                communication: 90,
                friendship: 88,
                marriage: 65
            },
            pros: "Great communication and emotional connection",
            cons: "Different approaches to long-term commitment"
        };
        generateCompatibilityChart(sampleCompatibility);
    }
});