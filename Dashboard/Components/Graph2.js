import React from 'react'
import Plotly from 'react-plotly.js'
import {Loader} from 'rsuite'


export default function Graph2({data, form}){
	const weighted = ['wSB', 'wRAA', 'wRC', 'wRC+'];
	const leagueList = ['H','1B','2B','3B','HR','R','RBI'];

	const [nonMVPStats, setNonMVPStats] = React.useState();
	const [MVPStats, setMVPStats] = React.useState();

	function MVPFill(list, mvp, form) {
		let NLstatus = form.NL? 'NL':false
		let ALstatus = form.AL? 'AL':false
		let NonMVPStats = [];
		for (let i=0; i<list.length;i++) {
			NonMVPStats.push(data.filter(person => (person.MVP === mvp && person.Season <= form.season[1] && 
				person.Season >= form.season[0] && (person.lgID === NLstatus || person.lgID === ALstatus)
			)).map((player) => (player[list[i]])));
		};
		return NonMVPStats
	};
	function Average(list) {
		return list.reduce((b, a) => Number(b) + Number(a), 0)/ list.length;
	}
	React.useEffect(() => {
		if (data) {
			form.nonMVP? setNonMVPStats([MVPFill(weighted,'0', form), MVPFill(leagueList,'0', form)]):
				setNonMVPStats([[[],[],[],[]],[[],[],[],[],[],[],[]]]);

			form.MVP? setMVPStats([MVPFill(weighted,'1', form), MVPFill(leagueList,'1', form)]):
				setMVPStats([[[],[],[],[]],[[],[],[],[],[],[],[]]]);
		};
	}, [data, form]);

	return (
		<div className='mvp-plot'>
		{data?
			<>
				<Plotly 
					data={[
						{
							x: weighted,
							y: MVPStats && MVPStats[0].map(stat => Average(stat)),
							type: 'scatter',
							mode: 'markers',
							name: 'MVP',
							marker: {color: '#F5F5DC'},
						},
						{
							x: weighted,
							y: nonMVPStats && nonMVPStats[0].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#D8BFD8'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Weighted Stats', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 550, width: 750, showlegend: false,
						font: {family: 'Courier New, monospace', size: 22, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
				/> 
				<Plotly 
					data={[
						{
							x: leagueList,
							y: MVPStats && MVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							name: 'MVP',
							mode: 'markers',
							marker: {color: '#F5F5DC'},
						},
						{
							x: leagueList,
							y: nonMVPStats && nonMVPStats[1].map(stat => Average(stat)),
							type: 'scatter',
							name: 'Non MVP',
							marker: {color: '#D8BFD8'},
						},
						{type: 'scatter', x: [], y: []},
					]}
					layout={{title: 'Classic Counting', boxmode:'group', paper_bgcolor:'rgba(0,0,0,0)', 
						plot_bgcolor:'transparent', height: 550, width: 1200, 
						font: {family: 'Courier New, monospace', size: 22, color: '#fffacd'},
						xaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'},
						yaxis: {gridcolor: '#a52a2a', linecolor: '#a52a2a', zerolinecolor: '#a52a2a'}}}
				/>

			</> : <div style = {{display: 'flex', marginTop: '86px'}}>
				<Loader size="lg"/><h1 style= {{marginLeft: '22px', color: '#F5F5DC'}}>Loading</h1>
			</div>
		}
		</div>
	)
}
