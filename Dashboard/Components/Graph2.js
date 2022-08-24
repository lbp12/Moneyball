import React from 'react'
import Plotly from 'react-plotly.js'

export default function Graph2({data, loading}){
	const weighted = ['wSB', 'wRAA', 'wRC', 'wRC+'];
	const Misc = ['Age','WAR'];
	const leagueList = ['H','1B','2B','3B','HR','R','RBI'];

	const [nonMVPStats, setNonMVPStats] = React.useState();
	const [MVPStats, setMVPStats] = React.useState();

	function MVPFill(list, mvp) {
		let NonMVPStats = [];
		for (let i=0; i<list.length;i++) {
			NonMVPStats.push(data.filter(person => person.MVP === mvp).map((player) => (player[list[i]])));
		};
		return NonMVPStats
	};
	function Average(list) {
		return list.reduce((b, a) => Number(b) + Number(a), 0)/ list.length;
	}
	React.useEffect(() => {
		if (loading !== true) {
			setNonMVPStats([MVPFill(leagueList,'0'),  MVPFill(Misc,'0'), MVPFill(weighted,'0')]);
			setMVPStats([MVPFill(leagueList,'1'), MVPFill(Misc,'1'), MVPFill(weighted,'1')]);

		};
	}, [loading]);

	nonMVPStats && console.log(nonMVPStats[0]);
	console.log(MVPStats);
	return (
		<div className='mvp-plot'>
		{!loading?
			<>
				<Plotly 
					data={[
						{
							x: Misc,
							y: MVPStats && MVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							name: 'MVP',
							mode: 'markers',
							marker: {color: '#F5F5DC'},
						},
						{
							x: Misc,
							y: nonMVPStats && nonMVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#D8BFD8'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Misc', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 900, width: 400, showlegend: false,
						font: {family: 'Courier New, monospace', size: 30, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a', fontcolor:'#fffacd'}}}
				/>
				<Plotly 
					data={[
						{
							x: weighted,
							y: MVPStats && MVPStats[2].map(stat => Average(stat)),
							type: 'scatter',
							mode: 'markers',
							name: 'MVP',
							marker: {color: '#F5F5DC'},
						},
						{
							x: weighted,
							y: nonMVPStats && nonMVPStats[2].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#D8BFD8'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Weighted Stats', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 900, width: 600, showlegend: false,
						font: {family: 'Courier New, monospace', size: 30, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
				/> 
				<Plotly 
					data={[
						{
							x: leagueList,
							y: MVPStats && MVPStats[0].map(stat => Average(stat)),
							type: 'scatter',
							name: 'MVP',
							mode: 'markers',
							marker: {color: '#F5F5DC'},
						},
						{
							x: leagueList,
							y: nonMVPStats && nonMVPStats[0].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#D8BFD8'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Classic Counting', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 900, width: 900, 
						font: {family: 'Courier New, monospace', size: 30, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
				/>

			</> : <h1>...Loading...</h1>
		}
		</div>
	)
}
