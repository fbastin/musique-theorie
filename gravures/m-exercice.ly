\version "2.24.3"
%% Fichier produit par outils/generer_mordants.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff  {
      \clef treble \time 4/4 \override TextScript.staff-padding = #4
      \key g \major g'4\mordent_\markup \small 1 a'8 b'8 c''4 b'4\mordent_\markup \small 2 | a'4 d''4\prall_\markup \small 3 c''4\mordent_\markup \small 4 b'4 | e''4\prall_\markup \small 5 d''8 c''8 a'4-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) \center-column { \musicglyph "scripts.mordent" \teeny \sharp }_\markup \small 6 b'4\prall_\markup \small 7 | fis'4\mordent_\markup \small 8 a'4 g'2\prallmordent_\markup \small 9
      \bar "|."
    }
  \layout {
    
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
