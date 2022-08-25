import React from 'react'
import Plotly from 'react-plotly.js'

export default function Graph2({data, loading, season, leagueStatus}){
	const weighted = ['wSB', 'wRAA', 'wRC', 'wRC+'];
	const leagueList = ['H','1B','2B','3B','HR','R','RBI'];

	const [nonMVPStats, setNonMVPStats] = React.useState();
	const [MVPStats, setMVPStats] = React.useState();

	function MVPFill(list, mvp, season, leagueStatus) {
		let NLstatus = leagueStatus.NL? 'NL':false
		let ALstatus = leagueStatus.AL? 'AL':false
		console.log(ALstatus)
		let NonMVPStats = [];
		for (let i=0; i<list.length;i++) {
			NonMVPStats.push(data.filter(person => (person.MVP === mvp && person.Season <= season[1] && 
				person.Season >= season[0] && person.lgID === NLstatus || person.lgID === ALstatus
		)).map((player) => (player[list[i]])));
		};
		return NonMVPStats
	};
	function Average(list) {
		return list.reduce((b, a) => Number(b) + Number(a), 0)/ list.length;
	}
	React.useEffect(() => {
		if (loading !== true) {
			setNonMVPStats([MVPFill(leagueList,'0', season, leagueStatus), MVPFill(weighted,'0', season, leagueStatus)]);
			setMVPStats([MVPFill(leagueList,'1', season, leagueStatus), MVPFill(weighted,'1', season, leagueStatus)]);
			console.log(season);
			console.log(data);
		};
	}, [loading, season, leagueStatus]);
	return (
		<div className='mvp-plot'>
		{!loading?
			<>
				<Plotly 
					data={[
						{
							x: weighted,
							y: MVPStats && MVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							mode: 'markers',
							name: 'MVP',
							marker: {color: '#F5F5DC'},
						},
						{
							x: weighted,
							y: nonMVPStats && nonMVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#DA70D6'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Weighted Stats', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 750, width: 750, showlegend: false,
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
							marker: {color: '#DA70D6'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Classic Counting', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 750, width: 900, 
						font: {family: 'Courier New, monospace', size: 30, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
				/>

			</> : <h1>...Loading...</h1>
		}
		</div>
	)
}
