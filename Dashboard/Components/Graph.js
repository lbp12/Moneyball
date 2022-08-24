import React from 'react'
import Plotly from 'react-plotly.js'

export default function Graph({data}){
	return (
		<div className='WAR-plot'>
		{data &&
			<Plotly // WAR vs Season
				data={[
					{
						x: data.filter(person => person.lgID === 'NL').map(player => (
											player.Season)),
						y: data.filter(person => person.lgID === 'NL').map(player => (
											player.WAR)),
						type: 'box',
						name: 'National League',
						marker: {color: '#D8BFD8'},
					},
					{
						x: data.filter(person => person.lgID === 'AL').map(player => (
											player.Season)),
						y: data.filter(person => person.lgID === 'AL').map(player => (
											player.WAR)),
						type: 'box',
						name: 'American League',
						marker: {color: '#F5F5DC'},
					},
					{type: 'box', x: [], y: []},
				]}
				layout={{title: 'WAR vs Season', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
						height: 900, width: 2000, font: {family: 'Courier New, monospace', size: 30, color: '#fffacd'}, 
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a', range:[2008,2021]}, 
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
			/>
		}
		</div>
	)
}


