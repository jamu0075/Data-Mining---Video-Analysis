from pstats import Stats

p = Stats('profile.tsv')
p.sort_stats('cumulative').print_stats(10)
