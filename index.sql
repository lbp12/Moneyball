SELECT X.* 
	INTO public."ALLSTATS"
	FROM (SELECT * FROM public."AL" 
		  UNION ALL 
		  SELECT * FROM public."NL") X;
		  
SELECT Y.* 
	INTO public."ALLMVPS"
	FROM (SELECT * FROM public."ALMVP"
		  UNION ALL 
		  SELECT * FROM public."NLMVP") Y;
		  
ALTER TABLE public."ALLSTATS"
	DROP COLUMN "key_fangraphs",
	DROP COLUMN "playerID",
	DROP COLUMN "awardID",
	DROP COLUMN "yearID";
