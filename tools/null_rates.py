"""Summarize a frozen control-star run; no independence assumption for plates."""
import math

def summarize(rows):
    ids=[r['star_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('one row per control star required')
    for r in rows:
        if not isinstance(r['plates'],int) or not isinstance(r['passing_groups'],int) or r['plates']<0 or r['passing_groups']<0:raise ValueError('nonnegative integer counts required')
        if r['plates']==0 and r['passing_groups']:raise ValueError('groups require plate coverage')
    eligible=[r for r in rows if r['plates']>0];plates=sum(r['plates'] for r in eligible);groups=sum(r['passing_groups'] for r in eligible)
    return dict(stars_total=len(rows),stars_with_plates=len(eligible),stars_flagged=sum(r['passing_groups']>0 for r in eligible),groups=groups,plates=plates,flagged_star_fraction=sum(r['passing_groups']>0 for r in eligible)/len(eligible) if eligible else None,groups_per_thousand_plates=1000*groups/plates if plates else None)
